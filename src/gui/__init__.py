# src/gui/__init__.py
# Initializes the windows


# Imports
from PySide6.QtWidgets import QApplication, QMainWindow

from . import ui_start

# Definitions

# Window handlers
class StartWindow(QMainWindow, ui_start.Ui_MainWindow):
    def __init__(self, app: QApplication):
        # Init
        
        super(StartWindow, self).__init__()
        self.setupUi(self)
        
        self.app = app
        
        # Button connections
        self.setupButton.clicked.connect(self.setup_ui_start)
    
    
    def closeEvent(self, event) -> None:
        self.app.quit()


def create_windows() -> None:
    pass