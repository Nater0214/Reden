# src/p2p/src/my_node/src/node.py
# Handles nodes and connections between nodes


# Imports
from __future__ import annotations

import datetime
import hashlib
import json
from os import mkdir, path
from pathlib import Path
from random import choice

from getmac import get_mac_address
from p2pnetwork.node import Node

from src import get_ifaces, settings, thread_wrap

from .node_connection import NodeConnection


# Definitions
def get_nodes_from_json(mac: str) -> dict:
    """Get the nodes"""
    
    # Create n-chain directory if it doesn't exist
    if not path.exists(nchain_path := path.join(str(Path.home()), "n-chain")):
        mkdir(path.join(str(Path.home()), "n-chain"))
    
    # Create mac directory if it doesn't exist
    if not path.exists(path.join(nchain_path, mac)):
        mkdir(path.join(nchain_path, mac))
    
    # Create the nodes file if it doesn't exist
    if not path.exists(nodes_path := path.join(nchain_path, mac, "nodes.json")):
        with open(nodes_path, 'wt') as file:
            json.dump(
                {
                    "local-node": None,
                    "known-nodes": None
                },
            file, indent=4)

    # Return node json data
    with open(nodes_path, 'rt') as file:
        json_data = json.load(file)
        
    return json_data


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
                    if any([our_node["id"] == recv_node["id"] for our_node in self.known_nodes]):
                        continue
                    
                    self.known_nodes.append(recv_node)
    
    
    # Properties
    def is_alive(self) -> bool:
        return self._is_alive
    
    
    # Methods
    def my_init(self, iface: dict) -> None:
        """My init"""
        
        # Get the mac address
        mac = get_mac_address(ip=get_ifaces()[iface]["default_gateway"])
        
        # Get the nodes from the file
        node_json = get_nodes_from_json(''.join(mac.split(':')))
        
        
        # Get node id from json or make a new one
        if node_json["local-node"]:
            node_id = node_json["local-node"]["id"]
        
        else:
            node_id = 'N' + hashlib.new("sha1", str(datetime.datetime.now()).encode()).hexdigest()
        
        node_port = settings.get_setting_value("port")
        
        self.ip = get_ifaces()[iface]["inet4"][0]

        # Add known nodes to a list
        if node_json["known-nodes"]:
            self.known_nodes = node_json["known-nodes"]
        
        else:
            self.known_nodes = []
        
        self.initialized = True
        self._out_messages = {}
        
        super().__init__(self.ip, node_port, node_id)
    
    
    def add_known_node(self, node: NodeConnection) -> None:
        self.known_nodes.append(
            {
                "ip": node.ip,
                "port": node.port,
                "id": node.node_id
            }
        )


    def connect_with_node(self, json_data: dict) -> bool:
        """Connect with a node"""
        
        return super().connect_with_node(json_data["ip"], json_data["port"])


    def connect_random(self, amount: int = 1) -> None:
        """Connect with an amount of random nodes"""
        
        for _ in range(amount):
            self.connect_with_node(choice(self.known_nodes))
    
    def create_new_connection(self, connection, id_, host, port):
        """Override this method to use my NodeConnection"""
        
        return NodeConnection(self, connection, id_, host, port)
    
    
    def add_node(self, ip: str, port: int) -> None:
        """Connect to a new node"""

        # Attempt to connect to node
        self.connect_with_node({"ip": ip, "port": port})
    
    
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
            "ip": node.ip,
            "port": node.port,
            "id": node.node_id
        }
    
    
    def save_json(self) -> None:
        """Save the known nodes and this node's id to a json file"""
        
        


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
        
        # Run node
        super().run()
    
    
    def stop(self) -> None:
        """Stop the node"""
        
        # Only run if the node is initialized
        if not self.initialized:
            return
        
        # Only run if running
        if not self._is_alive:
            raise
        
        # Set alive flag
        self._is_alive = False
        
        # Stop node
        super().stop()