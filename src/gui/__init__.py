# src/gui/__init__.py
# Initializes the windows


# Imports
from PySide6.QtWidgets import QApplication, QMainWindow

from .src import ui_start

# Definitions

# Window handlers
class StartWindow(QMainWindow, ui_start.Ui_MainWindow):
    """The start window"""
    
    def __init__(self, app: QApplication) -> None:
        """Init"""
        
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.update_ui_values()
        
        self.app = app
    
    
    def closeEvent(self, event) -> None:
        """Quit the app on window close"""
        
        self.app.quit()


    # Methods
    def update_ui_values(self) -> None:
        self.localNodeIPStat.setText(local_node.ip)
        self.localNodePortStat.setText(str(local_node.port))
        self.localNodeIDStat.setText(local_node.id)


def create_windows(app: QApplication, local_node_) -> None:
    """Create the windows"""
    
    # Create global variables
    global start_window
    global local_node
    
    # Set variable values
    local_node = local_node_
    start_window = StartWindow(app)