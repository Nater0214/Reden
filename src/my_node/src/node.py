# src/p2p/src/my_node/src/node.py
# Handles nodes and connections between nodes


# Imports
from __future__ import annotations

import json
from os import mkdir, path
from pathlib import Path
from random import choice
from time import sleep

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from getmac import get_mac_address
from p2pnetwork.node import Node

from src import func_cache, generate_id, get_ifaces, settings, thread_wrap

from .node_connection import NodeConnection


# Definitions
@func_cache()
def get_chain_dir(mac: str) -> str:
    """Get the directory of the chain"""
    
    # Create the n-chain directory if it doesn't exist
    if not path.exists(nchain_path := path.join(str(Path.home()), "n-chain")):
        mkdir(path.join(str(Path.home()), "n-chain"))
    
    # Create the mac directory if it doesn't exist
    if not path.exists(path.join(nchain_path, ''.join(mac.split(':')))):
        mkdir(path.join(nchain_path, ''.join(mac.split(':'))))
    
    # Return the path
    return path.join(nchain_path, ''.join(mac.split(':')))


def get_nodes_from_json(mac: str) -> dict:
    """Get the nodes"""
    
    # Get the path of the current chain
    current_chain_path = get_chain_dir(mac)
    
    # Create the nodes file if it doesn't exist
    if not path.exists(nodes_path := path.join(current_chain_path, "nodes.json")):
        with open(nodes_path, 'wt') as file:
            json.dump(
                {
                    "local-node": None,
                    "known-nodes": None
                },
            file, indent=4)

    # Get the node json data
    with open(nodes_path, 'rt') as file:
        json_data = json.load(file)
    
    # Return the json data
    return json_data


def get_node_data(mac: str) -> dict:
    """Get the data of every node"""
    
    # If the node info file does not exist return False
    if not path.exists(node_data_path := path.join(get_chain_dir(mac), "node-info.json")):
        return False
    
    # Get node data json from file
    with open(node_data_path, 'rt') as file:
        json_data = json.load(file)
    
    # Return the json data
    return json_data


def get_node_public_key(mac: str, id: str) -> ec.EllipticCurvePublicKey | bool:
    """Get the public key of a node"""
    
    # Get the node data
    if not (node_data := get_node_data(mac)):
        return False
    
    # Get the public key of the node
    try:
        public_key_bytes = bytes.fromhex(node_data[id]["public-key"])
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=backends.default_backend()
        )
    except KeyError:
        return False
    
    # Return the public key
    return public_key


def get_private_key(mac: str) -> ec.EllipticCurvePrivateKey:
    """Get the private key"""
    
    # Create a private key if it doesn't exist 
    if not path.exists(private_key_path := path.join(get_chain_dir(mac), "private.key")):
        private_key = ec.generate_private_key(ec.SECP256K1)
        with open(private_key_path, 'wb') as file:
            file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    
    # Get the private key
    with open(private_key_path, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None,
            backend=backends.default_backend()
        )
    
    return private_key


class LocalNode(Node):
    """The local node on this machine"""
    
    # Variables
    initialized = False
    
    
    def __init__(self):
        self._is_alive = False
        pass
    
    
    # Events
    def inbound_node_connected(self, node: NodeConnection) -> None:
        self.add_known_node(node)
    
    
    def outbound_node_connected(self, node: NodeConnection) -> None:
        self.add_known_node(node)
    
    
    def node_message(self, node: NodeConnection, data: dict):
        """Do stuff based on a node message"""
        
        # Node asked for something
        if data["action"] == "ask":
            # Node asked for known nodes
            if data["body"] == "KN":
                node.reply(data["msg-id"], self.known_nodes)
        
        
        # Node replied to something
        elif data["action"] == "reply":
            # Node replied with known nodes
            if self._out_messages[data["msg-id"]]["body"] == "KN":
                for recv_node in data["body"]:
                    if any(our_node["id"] == recv_node["id"] for our_node in self.known_nodes):
                        continue
                    
                    self.known_nodes.append(recv_node)
            
            self._out_messages.pop(data["msg-id"])
    
    
    # Properties
    def is_alive(self) -> bool:
        return self._is_alive
    
    
    # Methods
    def my_init(self, iface: dict) -> None:
        """My init"""
        
        # Get the mac address
        self.mac = get_mac_address(ip=get_ifaces()[iface]["default_gateway"])
        
        # Get the nodes from the file
        node_json = get_nodes_from_json(self.mac)
        
        # Get node id from json or make a new one
        if node_json["local-node"]:
            node_id = node_json["local-node"]["id"]
        
        else:
            node_id = generate_id('N')
        
        node_port = settings.get_setting_value("port")
        
        node_host = get_ifaces()[iface]["inet4"][0]
        
        # Add known nodes to a list
        if node_json["known-nodes"]:
            self.known_nodes = node_json["known-nodes"]
        
        else:
            self.known_nodes = []
        
        # Get the private key
        self.private_key = get_private_key(self.mac)
        
        # Set variables
        self.initialized = True
        self._out_messages = {}
        
        # Set debug flag
        self.debug = True
        
        super().__init__(node_host, node_port, node_id)
    
    
    def add_known_node(self, node: NodeConnection) -> None:
        if any(known_node["id"] == node.id for known_node in self.known_nodes):
            return
        
        self.known_nodes.append(
            {
                "host": node.host,
                "port": node.port,
                "id": node.id
            }
        )


    def connect_with_node(self, json_data: dict) -> bool:
        """Connect with a node"""
        
        return super().connect_with_node(json_data["host"], json_data["port"])


    def connect_random(self, amount: int = 1) -> None:
        """Connect with an amount of random nodes"""
        
        for _ in range(amount):
            self.connect_with_node(choice(self.known_nodes))
    
    def create_new_connection(self, connection, id_, host, port):
        """Override this method to use my NodeConnection"""
        
        return NodeConnection(self, connection, id_, host, port)
    
    
    def add_node(self, host: str, port: int) -> None:
        """Connect to a new node"""

        # Attempt to connect to node
        self.connect_with_node({"host": host, "port": port})
    
    
    def disconnect_all(self) -> None:
        """Disconnect from every node"""
        
        for node in self.nodes_outbound:
            self.disconnect_with_node(node)
    
    
    def ask_nodes(self, for_: str) -> None:
        """Ask every node for something"""
        
        for node in self.nodes_outbound:
            node: NodeConnection
            msg_data = node.ask(for_)
            self._out_messages[msg_data["msg-id"]] = msg_data
    
    
    def return_node_json(self, node: NodeConnection) -> dict:
        """Return a node's json data"""
        
        return {
            "host": node.host,
            "port": node.port,
            "id": node.id
        }
    
    
    def save_json(self) -> None:
        """Save the known nodes and this node's id to a json file"""
        
        out_nodes = [self.return_node_json(node) for node in self.nodes_outbound]
        
        with open(path.join(str(Path.home()), "n-chain", ''.join(self.mac.split(':')), "nodes.json"), 'wt') as file:
            json.dump({
                "known-nodes": out_nodes,
                "local-node": {
                    "id": self.id
                }
            }, file, indent=4)


    @thread_wrap("P2PNode")
    def run(self) -> None:
        """Run the node"""
        
        # Only run if the node is initialized
        if not self.initialized:
            return
        
        # Only run if not already running
        if self._is_alive:
            return
        
        # Set alive flag
        self._is_alive = True
        
        # Set running flag
        self._running = True
        
        # Run node
        super().run()
        
        # Set running flag
        self._running = False
    
    
    def stop(self) -> None:
        """Stop the node"""
        
        # Only run if the node is initialized
        if not self.initialized:
            return
        
        # Only run if running
        if not self._is_alive:
            return
        
        # Set alive flag
        self._is_alive = False
        
        # Stop node
        super().stop()
        
        # Wait for node to finish
        while self._running:
            sleep(0.1)