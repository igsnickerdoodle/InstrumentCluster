from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from pathlib import Path
import math, sys

### Local component imports
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))

from components.rpm.dd_rpm_1 import background_rpm, rpm_widget


class LeftDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_rpm = background_rpm()
        self.rpm_widget = rpm_widget()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.background_rpm.rpm_bg_a(painter)
        self.background_rpm.rpm_bg_indicators_a(painter)
        self.background_rpm.rpm_bg_indicators_b(painter)
        self.background_rpm.rpm_bg_indicators_c(painter)
        self.background_rpm.rpm_bg_text(painter)
        self.background_rpm.rpm_bg_b(painter)        
        self.rpm_widget.needle_widget(painter)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the background to black
        self.setStyleSheet("background-color: black;")


        # Create a ArcWidget instance
        self.arcWidget = LeftDisplay()

        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 1026, 600)

        # Create a QWidget and set it as the central widget
        central_widget = LeftDisplay()
        self.setCentralWidget(central_widget)

        # Create a QHBoxLayout, add the arc widget to it and add a stretch
        layout = QHBoxLayout()
        layout.addWidget(self.arcWidget)
        layout.addStretch(1)
        
        # Set the layout of the central widget
        central_widget.setLayout(layout)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())