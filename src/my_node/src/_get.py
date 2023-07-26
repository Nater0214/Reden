# src/my_node/src/_get.py


# Imports
import json
from os import mkdir, path
from pathlib import Path

from Crypto.PublicKey import ECC
from naters_utils.functions import func_cache


# Definitions
@func_cache()
def chain_dir(mac: str) -> str:
    """Get the directory of the chain"""
    
    # Create the n-chain directory if it doesn't exist
    if not path.exists(nchain_path := path.join(str(Path.home()), "n-chain")):
        mkdir(path.join(str(Path.home()), "n-chain"))
    
    # Create the mac directory if it doesn't exist
    if not path.exists(path.join(nchain_path, ''.join(mac.split(':')))):
        mkdir(path.join(nchain_path, ''.join(mac.split(':'))))
    
    # Return the path
    return path.join(nchain_path, ''.join(mac.split(':')))


def nodes_from_json(mac: str) -> dict:
    """Get the nodes"""
    
    # Get the path of the current chain
    current_chain_path = chain_dir(mac)
    
    # Create the nodes file if it doesn't exist
    if not path.exists(nodes_path := path.join(current_chain_path, "nodes.json")):
        with open(nodes_path, 'wt') as file:
            json.dump(
                {
                    "local-node": None,
                    "known-nodes": None
                },
            file, indent=4)

    # Get the node json data
    with open(nodes_path, 'rt') as file:
        json_data = json.load(file)
    
    # Return the json data
    return json_data


def node_data(mac: str) -> dict | bool:
    """Get the data of every node"""
    
    # If the node info file does not exist return False
    if not path.exists(node_data_path := path.join(chain_dir(mac), "node-data.json")):
        with open(node_data_path, 'wt') as file:
            json.dump({}, file, indent=4)
        return False
    
    # Get node data json from file
    with open(node_data_path, 'rt') as file:
        json_data = json.load(file)
    
    # Return the json data
    return json_data


def node_public_key(mac: str, id: str) -> ECC.EccKey | bool:
    """Get the public key of a node"""
    
    # Get the node data
    if not (node_data_json := node_data(mac)):
        return False
    
    # Get the public key of the node
    try:
        public_key = ECC.import_key(node_data_json[id]["public-key"], None, "p256")
    except KeyError:
        return False
    
    # Return the public key
    return public_key


def private_key(mac: str) -> tuple[ECC.EccKey, bool]:
    """Get the private key"""
    
    # Create a private key if it doesn't exist 
    if not path.exists(private_key_path := path.join(chain_dir(mac), "private.key")):
        private_key = ECC.generate(curve="p256")
        with open(private_key_path, 'wt') as file:
            file.write(private_key.export_key(format="PEM"))
        
        new_key = True
    
    else:
        new_key = False
    
    # Get the private key
    with open(private_key_path, 'rt') as file:
        private_key = ECC.import_key(file.read(), None, "p256")
    
    return private_key, new_key