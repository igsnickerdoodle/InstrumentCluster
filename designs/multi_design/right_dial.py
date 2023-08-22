from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from pathlib import Path
import sys

### Local component imports
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))
from components.speed.dd_speed_1 import background_speed, speed_widget


class RightDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_speed = background_speed()
        self.speed_widget = speed_widget()

               
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.background_speed.speed_bg_a(painter)
        self.background_speed.speed_bg_indicators_a(painter)
        self.background_speed.speed_bg_indicators_b(painter)
        self.background_speed.speed_bg_indicators_c(painter)
        self.background_speed.speed_bg_text(painter)
        self.background_speed.speed_bg_b(painter)
        self.speed_widget.speed_needle(painter)

 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the background to black
        self.setStyleSheet("background-color: black;")

        # Create a central widget
        self.central_widget = QWidget()

        # Create a Speedometer instance
        self.arcWidget = RightDisplay()

        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 800, 480)

        # Create a QHBoxLayout
        layout = QHBoxLayout()

        # Add a stretch factor to the layout to push the widget to the right

        # Add the widget to the layout
        layout.addWidget(self.arcWidget)

        # Set the layout of the central widget
        self.central_widget.setLayout(layout)

        # Set the central widget of the MainWindow
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())