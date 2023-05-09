# src/__init__.py
# For cleaner imports


# Set __all__
__all__ = ["func_cache", "generate_id", "get_ifaces", "thread_wrap"]


# Imports
import base64
import hashlib
import time

from ._func_cache import func_cache
from ._get_ifaces import get_ifaces
from ._thread_wrap import thread_wrap


# Definitions
def generate_id(prefix: str = None):
    """Generate a unique ID"""
    
    # Make the unique id
    unique_id = base64.b64encode(bytes.fromhex(hashlib.new("sha1", int(time.time()*100).to_bytes(5)).hexdigest()), b"_-").decode()[:-1]
    
    # Return it with optional prefix
    return ((prefix + ":") if prefix else "") + unique_id
