# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me
# I know libraries exist; I wanted to challenge myself


# Imports
from os.path import exists
from os import mkdir

import datetime
import hashlib
import json
from getmac import getmac
from .src import my_node as my_node


# Definitions
def start() -> bool:
    """Start p2p"""
    
    local_node = my_node.LocalNode()