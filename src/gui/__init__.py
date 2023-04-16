# src/gui/__init__.py
# Initializes the windows


# Imports
from PySide6.QtWidgets import QApplication, QMainWindow

from .src import ui_add_node, ui_start


# Definitions
class InputError(Exception):
    """An error with user input"""
    
    def __init__(self, message: str) -> None:
        self._message = message
    
    def __str__(self) -> str:
        return self._message


# Window handlers
class StartWindow(QMainWindow, ui_start.Ui_MainWindow):
    """The start window"""
    
    def __init__(self, app: QApplication) -> None:
        """Init"""
        
        # Setup UI
        super(StartWindow, self).__init__()
        self.setupUi(self)
        self.update_ui_values()
        
        # Set app variable
        self.app = app
        
        # Button handlers
        self.addNodeButton.clicked.connect(self.open_add_node_window)
    
    
    # Events
    def closeEvent(self, event) -> None:
        """Quit the app on window close"""
        
        self.app.quit()
    
    
    # Button methods
    def open_add_node_window(self) -> None:
        """Open the add node window"""
        
        add_node_window.show()


    # Methods
    def update_ui_values(self) -> None:
        self.localNodeIPStat.setText(local_node.ip)
        self.localNodePortStat.setText(str(local_node.port))
        self.localNodeIDStat.setText(local_node.id)


class AddNodeWindow(QMainWindow, ui_add_node.Ui_MainWindow):
    """The node adding window"""
    
    def __init__(self) -> None:
        """Init"""
        
        # Setup UI
        super(AddNodeWindow, self).__init__()
        self.setupUi(self)
        
        # Add button handler(s)
        self.addButton.clicked.connect(self.add_node)
    
    
    # Button methods
    def add_node(self) -> None:
        """Add a node"""
        
        # Get values
        ip = self.IPInput.text()
        port = self.portInput.text()
        
        # Validate values
        try:
            # IP exists
            if not ip:
                raise InputError("IP is required")

            # Port exists
            if not port:
                raise InputError("Port is required")
            
            # IP is valid
            if len(octets := (ip.split("."))) != 4:
                raise InputError("IP is not valid")

            # IP in range
            if not all([0 <= int(octet) <= 255 for octet in octets]):
                raise InputError("IP is not valid")

            # Port is valid
            try:
                port = int(port)
            except ValueError:
                raise InputError("Port is not valid")

            # Port in range
            if not (0 < port < 65536):
                raise InputError("Port is not valid")
            
        except InputError as e:
            self.statusLabel.setText(str(e))
        
        else:
            # Add node
            local_node.add_node(ip, port)
            
            # Clear input fields
            self.IPInput.clear()
            self.portInput.clear()
            
            # Close window
            self.close()


def create_windows(app: QApplication, local_node_) -> None:
    """Create the windows"""
    
    # Create global variables
    global start_window
    global add_node_window
    global local_node
    
    # Set variable values
    local_node = local_node_
    start_window = StartWindow(app)
    add_node_window = AddNodeWindow()