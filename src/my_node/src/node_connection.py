# src/my_node/src/node_connection.py
# My override of the node connection


# Imports
import datetime
import hashlib
import p2pnetwork.nodeconnection


# Definitions
class NodeConnection(p2pnetwork.nodeconnection.NodeConnection):
    """My override of the node connection"""
    
    
    # Methods
    def ask(self, for_: str) -> dict:
        """Ask the connection for something"""
        
        # Create a message id
        msg_id = 'M' + hashlib.new("sha1", str(datetime.datetime.now()).encode()).hexdigest()
        
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
    
    
    def reply(self, msg_id: str, body: None | bool | int | str | list | dict):
        """Reply to a message from another node"""
        
        self.send({
            "action": "reply",
            "msg-id": msg_id,
            "body": body
        })