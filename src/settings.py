# src/settings.py
# Stuff for handling settings


# Imports
import json
from os import mkdir, path

from naters_utils.functions import func_cache


# Definitions
@func_cache()
def _get_settings_path() -> str:
    """Get the path to the settings file and make sure it exists"""
    
    # Make sure store exists
    if not path.exists((store_path := path.join(path.realpath(path.dirname(__file__)), "..", "store"))):
        mkdir(store_path)
    
    # Make sure DO NOT EDIT file exists
    if not path.exists((do_not_edit_path := path.join(store_path, "DO_NOT_EDIT_YOURSELF"))):
        with open(do_not_edit_path, 'wt') as file:
            file.write("DO NOT EDIT THE SETTINGS FILE YOURSELF")
    
    # Make sure settings file exists
    if not path.exists((settings_path := path.join(store_path, "settings.json"))):
        with open(settings_path, 'wt') as file:
            json.dump({key: None for key in ["interface", "port", "node-auto-start", "max-known-nodes", "max-connected-nodes"]}, file, indent=4)
    
    return path.join(settings_path)


def get_setting_value(name: str) -> None | bool | int | str | list | dict:
    """Get a settings value by it's name"""
    
    # Get json from from file
    with open(_get_settings_path(), 'rt') as file:
        json_data = json.load(file)
    
    # Try to get value, raise error if it doesn't exist
    try:
        value = json_data[name]
    except KeyError:
        raise KeyError(f"No setting with name '{name}' exists")
    
    return value


def set_setting_value(name: str, value: None | bool | int | str | list | dict) -> None:
    """Update a settings value by it's name"""
    
    # Make sure setting exists
    get_setting_value(name)
    
    # Get json from from file
    with open(_get_settings_path(), 'rt') as file:
        json_data = json.load(file)
    
    # Change value
    json_data[name] = value
    
    # Write json to file
    with open(_get_settings_path(), 'wt') as file:
        json.dump(json_data, file, indent=4)