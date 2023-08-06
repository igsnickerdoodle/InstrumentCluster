import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from twisted.internet import reactor
from vncdotool.client import VNCDoToolFactory

class AndroidVNC(QWidget):
    def __init__(self, server, password=None):
        super().__init__()

        # Initialize VNC client
        self.client = VNCDoToolFactory()
        self.client.password = password

        # Connect to VNC server
        reactor.connectTCP(server, 5900, self.client)

        # Setup display
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Update display every time a frame is received
        self.client.deferred.addCallback(self.update_display)

        # Start Twisted reactor in separate thread, because it blocks
        QTimer.singleShot(0, self.start_reactor)

    def start_reactor(self):
        if not reactor.running:
            reactor.run(installSignalHandlers=0)  # 0 to allow PyQt to handle signals

    def update_display(self, protocol):
        # Convert raw VNC frame to QPixmap
        image = QImage(protocol.framebuffer, protocol.width, protocol.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        # Display QPixmap
        self.label.setPixmap(pixmap)

        # Schedule next frame update
        protocol.frameReceived.addCallback(self.update_display)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    viewer = AndroidVNC('localhost')
    viewer.show()

    sys.exit(app.exec_())
