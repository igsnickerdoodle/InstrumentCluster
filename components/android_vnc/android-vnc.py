import sys
import logging
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, QThread
from twisted.internet import reactor
from vncdotool.client import VNCDoToolFactory

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ReactorThread(QThread):
    def run(self):
        logging.debug("Starting the reactor thread.")
        if not reactor.running:
            reactor.run(installSignalHandlers=False)  # Disable signal handling to not interfere with PyQt
        logging.debug("Reactor thread started.")

class AndroidVNC(QWidget):
    def __init__(self):
        super().__init__()
        logging.debug("Initializing the AndroidVNC class.")

        # Configuration
        server = '10.84.40.13'  # Replace with your VNC server address
        port = 5901             # Replace with your VNC server port
        password = 'Empl0y3d1!'  # Replace with your VNC password

        logging.debug(f"Connecting as to VNC server at {server}:{port} with password {password}.")

        # Initialize VNC client
        self.client = VNCDoToolFactory()
        self.client.password = password

        # Connect to VNC server
        reactor.connectTCP(server, port, self.client)

        # Setup display
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.client.deferred.addCallback(self.update_display)

        # Set the window geometry (position and size)
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Setup and start the reactor thread
        self.reactor_thread = ReactorThread()
        self.reactor_thread.start()

    def update_display(self, protocol):
        image = QImage(protocol.framebuffer, protocol.width, protocol.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        protocol.frameReceived.addCallback(self.update_display)

if __name__ == '__main__':
    logging.debug("Application start.")
    app = QApplication(sys.argv)
    viewer = AndroidVNC()
    viewer.show()
    sys.exit(app.exec_())
