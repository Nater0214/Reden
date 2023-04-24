# src/gui/__init__.py
# Initializes the windows


# Imports
from time import sleep

from getmac import get_mac_address
from PySide6.QtWidgets import QApplication, QMainWindow

from src import get_ifaces, p2p, settings, thread_wrap

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
        self.values_ready = False
        self.update_ui_values()
        
        # Set app variable
        self.app = app
        
        # Button handlers
        self.nodeStartButton.clicked.connect(self.start_local_node)
        self.addNodeButton.clicked.connect(self.open_add_node_window)
        self.saveSettingsButton.clicked.connect(self.save_settings)
    
    
    # Events
    def closeEvent(self, event) -> None:
        """Quit the app on window close"""
        
        self.app.quit()
    
    
    # Button methods
    def start_local_node(self) -> None:
        """Start the local node"""
        
        # Get the interface
        iface = settings.get_setting_value("interface")
        
        # Get the mac address of the default gateway
        mac = get_mac_address(ip=get_ifaces()[iface]["default_gateway"])
        
        # Start the local node
        global local_node
        local_node = p2p.start(''.join(mac.split(':')))
        
        # Update the ui values
        self.update_ui_values()


    def open_add_node_window(self) -> None:
        """Open the add node window"""
        
        add_node_window.show()

    
    def save_settings(self) -> None:
        """Save the settings"""
        
        # Interface
        settings.set_setting_value("interface", self.interfaceBox.currentText())


    # Methods
    @thread_wrap("UiUpdateThread")
    def update_ui_values(self) -> None:
        """Update the UI values"""
        
        # Update stats
        if local_node:
            self.localNodeIPStat.setText(local_node.ip)
            self.localNodePortStat.setText(str(local_node.port))
            self.localNodeIDStat.setText(local_node.id)
        
        # Disable node start button if no interface
        if not settings.get_setting_value("interface"):
            self.nodeStartButton.setEnabled(False)
            
        else:
            self.nodeStartButton.setEnabled(True)
        
        # Flag values as not ready
        self.values_ready = False
        self.saveSettingsButton.setEnabled(False)
        
        # Update settings selection
        self.interfaceBox.clear()
        for iface in get_ifaces().keys():
            self.interfaceBox.addItem(iface)
        if (iface := settings.get_setting_value("interface")):
            self.interfaceBox.setCurrentText(iface)
        else:
            self.interfaceBox.setCurrentIndex(0)
        
        # Flag values as ready
        self.values_ready = True
        self.saveSettingsButton.setEnabled(True)
    
    
    def await_values_ready(self) -> None:
        """Wait for ui values to be ready"""
        
        # Wait for value
        while not self.values_ready:
            sleep(0.1)


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


def create_windows(app: QApplication) -> None:
    """Create the windows"""
    
    # Create global variables
    global start_window
    global add_node_window
    global local_node
    
    # Set variable values
    local_node = None
    start_window = StartWindow(app)
    add_node_window = AddNodeWindow()