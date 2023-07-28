# Needed imports for functioning instrument cluster
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

## Module Imports
from .components import Tachometer



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 1920, 480)

        # Load the pixmap from the file
        pixmap = QPixmap('Instrument-Cluster-Single-Display/resources/background.jpg')

        # Create a QLabel, set the pixmap, and set it as the central widget
        label = QLabel()
        label.setPixmap(pixmap.scaled(1920, 480, Qt.IgnoreAspectRatio))

        # Set QLabel as central widget and set QGridLayout for central widget
        self.setCentralWidget(label)
        layout = QGridLayout(label)

        # Create the Tachometer and Speedometer instances with transparent backgrounds
        self.tachometer = Tachometer()

        self.tachometer.setAttribute(Qt.WA_TranslucentBackground, True)

        # Add widgets to layout at specific grid locations
        layout.addWidget(self.tachometer, 1, 0, 1, 2)  # Grid (row=1, col=0, rowspan=1, colspan=2)       
    def paintEvent(self, event):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
