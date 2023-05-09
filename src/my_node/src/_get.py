# src/my_node/src/_get.py


# Imports
import json
from os import mkdir, path
from pathlib import Path

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from src import func_cache


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


def node_data(mac: str) -> dict:
    """Get the data of every node"""
    
    # If the node info file does not exist return False
    if not path.exists(node_data_path := path.join(chain_dir(mac), "node-info.json")):
        return False
    
    # Get node data json from file
    with open(node_data_path, 'rt') as file:
        json_data = json.load(file)
    
    # Return the json data
    return json_data


def node_public_key(mac: str, id: str) -> ec.EllipticCurvePublicKey | bool:
    """Get the public key of a node"""
    
    # Get the node data
    if not (node_data := node_data(mac)):
        return False
    
    # Get the public key of the node
    try:
        public_key_bytes = bytes.fromhex(node_data[id]["public-key"])
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            password=None,
            backend=backends.default_backend()
        )
    except KeyError:
        return False
    
    # Return the public key
    return public_key


def private_key(mac: str) -> ec.EllipticCurvePrivateKey:
    """Get the private key"""
    
    # Create a private key if it doesn't exist 
    if not path.exists(private_key_path := path.join(chain_dir(mac), "private.key")):
        private_key = ec.generate_private_key(ec.SECP256K1)
        with open(private_key_path, 'wb') as file:
            file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
    
    # Get the private key
    with open(private_key_path, 'rb') as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None,
            backend=backends.default_backend()
        )
    
    return private_key