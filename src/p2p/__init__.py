# src/p2p/__init__.py
# Peer-to-peer stuff
# Written by me
# I know libraries exist; I wanted to challenge myself


# Imports
import datetime
import hashlib
import json
from os import mkdir
from os.path import exists

from getmac import getmac

from . import exceptions
from .src import my_node as my_node


# Definitions
def start() -> bool:
    """Start p2p"""
    
    local_node = my_node.LocalNode()