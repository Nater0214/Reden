# main.py
# Reden
# A LAN messaging platform


# Imports
import sys

from PySide6 import QtWidgets

import src.gui as gui


# Definitions
def main() -> None:
    """Main"""
    
    # Create Qt app
    app = QtWidgets.QApplication(sys.argv)
    
    # Create the windows
    gui.create_windows(app)
    
    # Show the start window
    gui.start_window.show()
    
    # Start app and exit with code
    sys.exit(app.exec())


# Run
if __name__ == "__main__":
    main()