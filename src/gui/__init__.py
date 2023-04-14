# src/gui/__init__.py
# Initializes the windows


# Imports
from PySide6.QtWidgets import QApplication, QMainWindow

from .src import ui_start

# Definitions

# Window handlers
class StartWindow(QMainWindow, ui_start.Ui_MainWindow):
    """The start window"""
    
    def __init__(self, app: QApplication):
        """Init"""
        
        super(StartWindow, self).__init__()
        self.setupUi(self)
        
        self.app = app
    
    
    def closeEvent(self, event) -> None:
        """Quit the app on window close"""
        
        self.app.quit()


def create_windows(app: QApplication) -> None:
    """Create the windows"""
    
    # Create global variables
    global start_window
    
    # Set variable values
    start_window = StartWindow(app)