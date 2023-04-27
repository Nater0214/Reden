# build.py
# Builds the project


# Imports
import os
import re
from argparse import ArgumentParser
import shutil

import PyInstaller.__main__


# Definitions
def main(args):
    """Main"""
    
    # Get name
    name = args.name
    
    # Build the project with PyInstaller
    print(f"Building the project {name}:")
    PyInstaller.__main__.run([
        "--noconfirm",
        f"{name}.spec"
    ])
    
    print("Organizing Output")
    files = list(filter(re.compile(r"^.*\.pyd$|^.*(?<!python\d)(?<!python\d{3})\.dll$").match, os.listdir(out_path := os.path.join(os.path.realpath(os.path.dirname(__file__)), "dist", name))))
    os.mkdir(lib_path := os.path.join(out_path, "lib"))
    for file in files:
        shutil.move(os.path.join(out_path, file), os.path.join(lib_path, file))


# Run
if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("name", help="Name of the project")

    main(arg_parser.parse_args())