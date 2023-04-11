# src/p2p/src/my_node.py
# Handles nodes and connections between nodes
# If this gets to complicated I'll make it a package


# Imports
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
        if json_data:
            node_id = json_data["local-node"]["id"]
        else:
            node_id = hashlib.new("sha1", str(datetime.datetime.now()).encode()).hexdigest()

        # Initialize node
        super().__init__(socket.gethostbyname(socket.gethostname()), 56787, node_id)
    
    
    # Methods
    def connect_with_node(self, node):
        """Connect with a node"""
        
        return super().connect_with_node(node.host, 56787)


class PeerNode:
    """A connected peer node"""

    def __init__(self, json_data: dict) -> None:
        """Create a connected peer node
        Really just a container for the data associated with it"""
        
        # Initialize node
        self.ip = json_data["ip"]
        self.id = json_data["id"]