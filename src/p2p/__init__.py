# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me


# Imports
import json
from os import mkdir, path
from pathlib import Path

from .src import my_node as my_node


# Definitions
def get_nodes_from_json(mac: str) -> dict:
    """Get the nodes"""
    
    # Create n-chain directory if it doesn't exist
    if not path.exists(nchain_path := (path.join(str(Path.home()), "n-chain"))):
        mkdir(path.join(str(Path.home()), "n-chain"))
    
    # Create the nodes file if it doesn't exist
    if not path.exists(nodes_path := (path.join(nchain_path, mac, "nodes.json"))):
        with open(nodes_path, 'wt') as file:
            json.dump(
                {
                    "local-node": None,
                    "known-nodes": None
                },
            file)

    # Return node json data
    with open(nodes_path, 'rt') as file:
        json_data = json.load(file)
        
    return json_data


def start(mac: str) -> my_node.LocalNode:
    """Start p2p"""
    
    # Get the nodes from the file
    nodes_json = get_nodes_from_json(mac)
    
    # Create local node
    global local_node
    local_node = my_node.LocalNode(nodes_json)
    
    # Start the local node
    local_node.run()
    
    # Return local node
    return local_node


def conclude() -> None:
    """Stop p2p"""
    
    # Disconnect all nodes
    local_node.disconnect_all()
    
    # Get the nodes json
    local_node.get_json()