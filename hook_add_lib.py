# add_lib.py
# Enables a cleaner project structure after being built
# Allows all libraries to be in the lib folder


# Imports
import os
import sys


# Add lib folder to path
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lib'))