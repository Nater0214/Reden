# src/p2p/src/my_node/__init__.py
# For importing purposes


# Imports
from .src.node import LocalNode

# from .src.node_list import NodeList


# Definitions
def return_json(nodes: NodeList) -> dict:
    """Return the json form of all of the nodes"""
    
    json_data = {}