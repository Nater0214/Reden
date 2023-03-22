# main.py
# Reden
# A LAN messaging platform


# Imports
import sys

from PySide6 import QtWidgets

import src.gui as gui
import src.p2p as p2p


# Definitions
def main() -> None:
    """Main"""
    
    # Start p2p
    success = p2p.start()
    
    # Raise error if no success
    if not success:
        raise p2p.errors.P2PStartError("P2P was not able to start.")
    
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