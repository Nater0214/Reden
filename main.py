# main.py
# Reden
# A LAN messaging platform


# Imports
import sys

import PySide6

from src import gui as gui
from src import p2p as p2p


# Definitions
def main() -> None:
    """Main"""
    
    # Create Qt app
    app = PySide6.QtWidgets.QApplication(sys.argv)
    
    # Create the windows
    gui.create_windows(app)
    
    # Show the start window
    gui.start_window.show()
    
    # Start app and get exit code
    exit_code = app.exec()
    
    # Stop p2p
    p2p.conclude()
    
    # Exit with code
    sys.exit(exit_code)


# Run
if __name__ == "__main__":
    main()