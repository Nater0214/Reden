# src/p2p/src/my_node/node_list.py
# Contains the NodeList object


# Imports
from random import choice

from . import LocalNode, PeerNode


# Definitions
class NodeList(list):
    """A list of nodes"""
    
    def __init__(self, json_data: dict) -> None:
        """Create a list of nodes"""
        
        # Get peer nodes if there are any
        if json_data["known-nodes"]:
            for node_data in json_data["known-nodes"]:
                self.append(PeerNode(node_data))
        
        # Get local node
        self.local_node = LocalNode(json_data["local-node"])
    
    
    # Methods
    def connect_random(self, amount: int = 1) -> None:
        """Connect with some random known nodes"""
        
        for _ in range(amount):
            self.local_node.connect_with_node(choice(self))