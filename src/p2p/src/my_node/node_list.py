# src/p2p/src/my_node/node_list.py
# Contains the NodeList object


# Imports
from .node import PeerNode


# Definitions
class NodeList(list):
    """A list of nodes"""
    
    def __init__(self, json_data: dict) -> None:
        for entry in json_data["known-nodes"]:
            pass
