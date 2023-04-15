# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me


# Imports
import json
from os import mkdir, path
from pathlib import Path

from .src import my_node as my_node


# Variables
local_node = None


# Definitions
def get_nodes_from_json() -> dict | None:
    """Get the nodes"""
    
    # Create n-chain directory if it doesn't exist
    if not path.exists(path.join(str(Path.home()), "n-chain")):
        mkdir(path.join(str(Path.home()), "n-chain"))
    
    # Create the nodes file if it doesn't exist
    if not path.exists(path.join(str(Path.home()), "n-chain", "nodes.json")):
        with open(path.join(str(Path.home()), "n-chain", "nodes.json"), 'wt') as file:
            json.dump(
                {
                    "local-node": None,
                    "known-nodes": None
                },
            file)

    # Return node json data
    with open(path.join(str(Path.home()), "n-chain", "nodes.json"), 'rt') as file:
        json_data = json.load(file)
        
    return json_data


def start() -> bool:
    """Start p2p"""
    
    # Get the nodes from the file
    nodes_json = get_nodes_from_json()
    
    # Create local node
    global local_node
    local_node = my_node.LocalNode(nodes_json)
    
    # Return success
    return True


def stop() -> None:
    """Stop p2p"""
    
    # Disconnect all nodes
    local_node.disconnect_all()
    
    # Get the nodes json
    local_node.get_json()