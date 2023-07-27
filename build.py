# build.py
# Builds the project


# Imports
import os
import py_compile
import re
import shutil
from argparse import ArgumentParser

import PyInstaller.__main__


# Definitions
def main():
    """Main"""
    
    # Build the project with PyInstaller
    print(f"Building the project {name}:")
    PyInstaller.__main__.run([
        "--noconfirm",
        f"reden.spec"
    ])
    
    # Organize the output
    print("Organizing Output")
    files = list(filter(re.compile(r"^.*\.pyd$|^.*(?<!python\d)(?<!python\d{3})\.dll$|^.*\.so(\.\d+)+$").match, os.listdir(out_path := os.path.join(os.path.realpath(os.path.dirname(__file__)), "dist", name))))
    os.mkdir(lib_path := os.path.join(out_path, "lib"))
    for file in files:
        shutil.move(os.path.join(out_path, file), os.path.join(lib_path, file))
        print(f"{os.path.join(out_path, file)} -> {os.path.join(lib_path, file)}")
    
    # Compile src folder
    print("Compiling src")
    for root, dirs, files in os.walk(os.path.join(os.path.realpath(os.path.dirname(__file__)), "dist", name, "src")):
        for file in files:
            if re.search(r"\.py$", file_path := os.path.join(root, file)):
                py_compile.compile(file_path, f"{file_path}c")
                print(f"{file_path} -> {file_path}c")
                os.remove(file_path)
    
    # Remove pycaches
    print("Removing pycaches")
    for root, dirs, files in os.walk(os.path.join(os.path.realpath(os.path.dirname(__file__)), "dist", name, "src")):
        for dir_ in dirs:
            if re.search(r"__pycache__/?$", os.path.join(root, dir_)):
                shutil.rmtree(os.path.join(root, dir_))
                print(f"{os.path.join(root, dir_)} X")


# Run
if __name__ == "__main__":
    main()