# src/p2p/src/my_node/src/node.py
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
            self._id = json_data["local-node"]["id"]
            self._port = json_data["local-node"]["port"]
        
        else:
            self._id = hashlib.new("sha1", str(datetime.datetime.now()).encode()).hexdigest()
            self._port = 56787
        
        self._ip = socket.gethostbyname(socket.gethostname())

        # Add known nodes to a list
        if json_data["known-nodes"]:
            self.known_nodes = json_data["known-nodes"]

        # Initialize node
        super().__init__(socket.gethostbyname(socket.gethostname()), self._port, self._id)
    
    
    # Properties
    @property
    def id(self) -> str:
        return self._id
    
    
    @property
    def port(self) -> int:
        return self._port
    
    
    @property
    def  ip(self) -> str:
        return self._ip
    
    
    # Methods
    def connect_with_node(self, json_data: dict) -> bool:
        """Connect with a node"""
        
        return super().connect_with_node(json_data["ip"], json_data["port"])
    
    
    def disconnect_all(self):
        """Disconnect from every node"""
        
        for node in self.nodes_outbound():
            self.disconnect_with_node(node)