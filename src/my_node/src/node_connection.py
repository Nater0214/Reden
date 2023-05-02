# src/my_node/src/node_connection.py
# My override of the node connection


# Imports
import p2pnetwork.nodeconnection


# Definitions
class NodeConnection(p2pnetwork.nodeconnection.NodeConnection):
    """My override of the node connection"""
    
    
    # Methods
    def ask(self, for_: str) -> None:
        """Ask the connection for something"""
        
        self.send({
            "action": "ask",
            "body": for_
        })