# src/p2p/src/my_node/src/node.py
# Handles nodes and connections between nodes


# Imports
from __future__ import annotations

import datetime
import hashlib
from random import choice
import socket

from p2pnetwork.node import Node


# Definitions
class LocalNode(Node):
    """The local node on this machine"""

    def __init__(self, node_json: dict) -> None:
        """Create a local node on this machine"""
        
        # Get id from json data, or use hash of current time if unavailable
        if node_json["local-node"]:
            node_id = node_json["local-node"]["id"]
            node_port = node_json["local-node"]["port"]
        
        else:
            node_id = hashlib.new("sha1", str(datetime.datetime.now()).encode()).hexdigest()
            node_port = 56787
        
        self.ip = socket.gethostbyname(socket.gethostname())

        # Add known nodes to a list
        if node_json["known-nodes"]:
            self.known_nodes = node_json["known-nodes"]

        # Initialize node
        super().__init__(self.ip, node_port, node_id)
    
    
    # Events
    def inbound_node_connected(self, node: Node) -> None:
        self.add_known_node(node)
    
    
    def outbound_node_connected(self, node: Node) -> None:
        self.add_known_node(node)
    
    
    # Methods
    def add_known_node(self, node: Node) -> None:
        self.known_nodes.append({
            "ip": node.ip,
            "port": node.port,
            "id": node.node_id
        })


    def connect_with_node(self, json_data: dict) -> bool:
        """Connect with a node"""
        
        return super().connect_with_node(json_data["ip"], json_data["port"])


    def connect_random(self, amount: int = 1) -> None:
        """Connect with an amount of random nodes"""
        
        for _ in range(amount):
            self.connect_with_node(choice(self.known_nodes))
    
    
    def add_node(self, ip: str, port: int) -> None:
        """Connect to a new node"""

        # Attempt to connect to node
        self.connect_with_node({"ip": ip, "port": port})
    
    
    def disconnect_all(self) -> None:
        """Disconnect from every node"""
        
        for node in self.nodes_outbound:
            self.disconnect_with_node(node)