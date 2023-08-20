from PyQt5.QtWidgets import QWidget, QApplication
import sys

from left_dial import LeftDisplay
from right_dial import RightDisplay


class DualDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: black;")
        self.left_display = LeftDisplay(self)
        self.right_display = RightDisplay(self)
        self.left_display.setGeometry(10, 10, 600, 600)  # You can adjust this as needed
        self.right_display.setGeometry(600, 10, 600, 600)  # You can adjust this as needed
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = DualDisplay()
    mainWin.show()
    sys.exit(app.exec_())
