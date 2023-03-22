# src/p2p/src/my_node.py
# Handles nodes and connections between nodes
# If this gets to complicated I'll make it a package


# Imports
from p2pnetwork.node import Node


# Definitions
class LocalNode(Node):
    """The local node on this machine"""


class PeerNode(Node):
    """A connected peer node"""