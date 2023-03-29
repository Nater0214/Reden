# src/p2p/src/my_node/__init__.py
# For importing purposes


# Imports
from ._node_list import NodeList
from .node import LocalNode, PeerNode


# Definitions
def return_json(local_node: LocalNode, other_nodes: NodeList[PeerNode]) -> dict:
    pass