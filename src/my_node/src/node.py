# src/p2p/src/my_node/src/node.py
# Handles nodes and connections between nodes


# Imports
from __future__ import annotations

import json
import socket
from os import mkdir, path
from pathlib import Path
from random import choice
from time import sleep

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import ECC
from getmac import get_mac_address
from p2pnetwork.node import Node

from src import func_cache, generate_id, get_ifaces, settings, thread_wrap

from . import _get as get
from .node_connection import NodeConnection


# Definitions
def update_node_data(mac: str, id_: str, *, public_key_str: str = None, alias: str = None) -> bool:
    """Updates the node data with the given data"""
    
    # Get the node data
    node_data = get.node_data(mac)
    
    # Return false if no data
    if node_data == False:
        return False
    
    # Initialize file if no data
    if not node_data:
        node_data = {
            id_: {
                "public-key": public_key_str,
                "alias": alias
            }
        }
    
    # Or update the node with an id
    else:
        # Set public key
        if public_key_str:
            node_data[id_]["public-key"] = public_key_str
        
        # Set alias
        if alias:
            node_data[id_]["alias"] = alias
    
    # Write data to file
    with open(path.join(get.chain_dir(mac), "node-data.json"), 'wt') as file:
        json.dump(node_data, file, indent=4)
    
    return True


class LocalNode(Node):
    """The local node on this machine"""
    
    # Variables
    initialized = False
    
    
    def __init__(self):
        self._is_alive = False
    
    
    # Events
    def inbound_node_connected(self, node: NodeConnection) -> None:
        self.add_known_node(node)
    
    
    def outbound_node_connected(self, node: NodeConnection) -> None:
        """Outbound node connected"""
        
        # Ask for node data if this is the first connected node ever
        if self.known_nodes == []:
            node.ft_get_node_data()
        
        self.add_known_node(node)
    
    
    def node_message(self, node: NodeConnection, data: str | bytes | dict) -> None:
        """Do stuff based on a node message"""
        
        # Check if a node is asking for first time node data
        if data == "ndplz":
            node.send(f"okh{repr(get.node_data(self.mac))}")
            return
        
        # Check if we got node data for the first time
        if isinstance(data, str):
            if data[0:3] == "okh":
                all_node_data = eval(data[3:])
                for node_id, node_data in all_node_data.items():
                    update_node_data(self.mac, node_id, public_key_str=node_data["public-key"], alias=node_data["alias"])
            return
        
        # Decrypt data
        cipher = PKCS1_OAEP.new(self.private_key)
        data = cipher.decrypt(data)
        
        # Node asked for an echo
        if data["action"] == "echo":
            node.reply(data["msg-id"], data["body"])
        
        # Node asked for something
        elif data["action"] == "ask":
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
        node_json = get.nodes_from_json(self.mac)
        
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
        self.private_key, self.is_new_key = get.private_key(self.mac)
        
        # Set variables
        self.initialized = True
        self._out_messages = {}
        
        super().__init__(node_host, node_port, node_id)
        
        self.debug = True
    
    
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
    
    
    def create_new_connection(self, connection: socket.sock, id_: str, host: str, port: int) -> NodeConnection:
        """Override this method to use my NodeConnection"""
        
        return NodeConnection(self, connection, id_, host, port, self.mac)
    
    
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
        
        if self.is_new_key:
            update_node_data(self.mac, self.id, public_key_str=self.private_key.public_key().export_key(format="PEM"))
        
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