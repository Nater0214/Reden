# src/p2p/src/my_node/__init__.py
# For importing purposes


# Imports
from ._node import LocalNode, PeerNode
from ._node_list import NodeList


# Definitions
def return_json(nodes: NodeList) -> dict:
    pass