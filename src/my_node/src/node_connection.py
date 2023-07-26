# src/my_node/src/node_connection.py
# My override of the node connection


# Imports
import socket

import p2pnetwork.nodeconnection
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import ECC
from naters_utils.functions import func_cache

from src import generate_id

from . import _get as get


# Definitions
class NodeConnection(p2pnetwork.nodeconnection.NodeConnection):
    """My override of the node connection"""
    
    def __init__(self, main_node, connection: socket.socket, id_: str, host: str, port: int, mac: str) -> None:
        """Init"""
        
        # Set mac
        self.mac = mac
        
        # Do init
        super().__init__(main_node, connection, id_, host, port)
    
    # Properties
    @property
    @func_cache()
    def public_key(self) -> ECC.EccKey | bool:
        """Get this node's public key"""
        
        # Get the public key from the node's data
        return get.node_public_key(self.mac, self.id)
    public_key: ECC.EccKey | bool
    
    
    # Methods
    def ask(self, for_: str) -> dict:
        """Ask the connection for something"""
        
        # Create a message id
        msg_id = generate_id('M')
        
        # Send the message
        self.send({
            "action": "ask",
            "msg-id": msg_id,
            "body": for_
        })
        
        # Return relevant information for tracking
        return {
            "action": "ask",
            "msg-id": msg_id,
            "body": for_
        }
    
    
    def reply(self, msg_id: str, body: None | bool | int | str | list | dict) -> None:
        """Reply to a message from another node"""
        
        self.send({
            "action": "reply",
            "msg-id": msg_id,
            "body": body
        })
    
    
    def ft_get_node_data(self) -> None:
        """Get the node data for the first time"""
        
        self.send("ndplz", _no_encryption=True)
    
    
    def send(self, data: str | dict | bytes, *, _no_encryption: bool = False):
        """Override the send method to use encryption"""
        
        # Encrypt the data using the node's public key
        # NOT IMPLEMENTED
        if _no_encryption:
            pass
        else:
            cipher = PKCS1_OAEP.new(self.public_key)
            data = cipher.encrypt(data)
        
        # Send the data
        super().send(data)