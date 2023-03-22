# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me
# I know libraries exist; I wanted to challenge myself


# Imports
from os.path import exists


from .src import my_node as my_node


# Definitions
def get_nodes() -> dict | None:
    """Get the nodes"""
    
    # Create the nodes file if it doesn't exist
    if not exists("store/nodes.json"):
        with open("store/nodes.json", 'wt') as file:
            file.write("{}")
        
        return None


def start() -> bool:
    """Start p2p"""
    
    # Get the nodes from the file
    nodes = get_nodes()
    
    # Create local node
    local_node = my_node.LocalNode()
    
    # Return success
    return True