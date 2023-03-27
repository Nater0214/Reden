# src/p2p/src/my_node/__init__.py
# For importing purposes


# Imports
from .node import LocalNode, PeerNode
from .node_list import NodeList


# Definitions
def get_json(local_node: LocalNode, other_nodes: NodeList[PeerNode]) -> dict:
    pass