# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me


# Imports
from os import mkdir, path
from pathlib import Path

from .src.my_node import node as node


# Definitions
def get_nodes() -> dict | None:
    """Get the nodes"""
    
    # Create n-chain directory if it doesn't exist
    if not path.exists(path.join(str(Path.home()), "n-chain")):
        mkdir(path.join(str(Path.home()), "n-chain"))
        
        return None
    
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
    local_node = node.LocalNode()
    
    # Return success
    return True