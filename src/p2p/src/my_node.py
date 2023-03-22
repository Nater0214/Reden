# src/p2p/src/my_node.py
# Handles nodes and connections between nodes
# If this gets to complicated I'll make it a package


# Imports
from p2pnetwork.node import Node
import socket


# Definitions
class LocalNode(Node):
    """The local node on this machine"""

    def __init__(self) -> None:
        """Create a local node on this machine"""
        
        super().__init__(socket.gethostbyname(socket.gethostname()), 56787)


class PeerNode(Node):
    """A connected peer node"""


