# src/get_ifaces.py
# Contains a function for getting network interfaces


# Imports
import re

import ifcfg

from src import func_cache


# Definitions
@func_cache()
def get_ifaces() -> dict:
    """Get the usable interfaces"""
    
    # Get interfaces
    all_ifaces = ifcfg.interfaces()
    out_ifaces = {}
    
    # Search through interfaces
    for key, value in all_ifaces.items():
        # Find interfaces by name
        if not re.search(r"[Ww]ireless|wlan|[Ee]thernet|eth", key):
            continue
        
        # Check if the interface has a default gateway
        try:
            _ = value["default_gateway"]
        
        except KeyError:
            continue
        
        # Add the interface to the output
        out_ifaces[key] = value
    
    # Return the interfaces
    
    return out_ifaces