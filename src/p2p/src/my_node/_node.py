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
            
        super().__init__(socket.gethostbyname(socket.gethostname()), 56787, node_id)


class PeerNode(Node):
    """A connected peer node"""


