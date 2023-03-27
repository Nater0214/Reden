# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me


# Imports
from os import path
from pathlib import Path

from .src.my_node import node as node


# Definitions
def get_nodes() -> dict | None:
    """Get the nodes"""
    
    # Create the nodes file if it doesn't exist
    if not path.exists(path.join(str(Path.home()), "n-chain", "nodes.json")):
        with open(path.join(str(Path.home()), "n-chain", "nodes.json"), 'x') as _:
                pass
        
        return None


def start() -> bool:
    """Start p2p"""
    
    # Get the nodes from the file
    nodes = get_nodes()
    
    # Create local node
    global local_node
    local_node = my_node.LocalNode()
    
    # Return success
    return True