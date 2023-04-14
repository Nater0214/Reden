# src/p2p/src/my_node.py
# Handles nodes and connections between nodes
# If this gets to complicated I'll make it a package


# Imports
from __future__ import annotations

import datetime
import hashlib
import socket

from p2pnetwork.node import Node


# Definitions
class LocalNode(Node):
    """The local node on this machine"""

    def __init__(self, json_data: dict | None = None) -> None:
        """Create a local node on this machine"""
        
        # Get id from json data, or use hash of current time if unavailable
        if json_data["local-node"]:
            node_id = json_data["local-node"]["id"]
            node_port = json_data["local-node"]["port"]
        
        else:
            node_id = hashlib.new("sha1", str(datetime.datetime.now()).encode()).hexdigest()
            node_port = 56787

        # Add known nodes to a list
        if json_data["known-nodes"]:
            self.known_nodes = json_data["known-nodes"]

        # Initialize node
        super().__init__(socket.gethostbyname(socket.gethostname()), node_port, node_id)
    
    
    # Methods
    def connect_with_node(self, json_data: dict) -> bool:
        """Connect with a node"""
        
        return super().connect_with_node(json_data["ip"], json_data["port"])
    
    
    def disconnect_all(self):
        """Disconnect from every node"""
        
        for node in self.nodes_outbound():
            self.disconnect_with_node(node)