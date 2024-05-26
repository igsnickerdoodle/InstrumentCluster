from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from datetime import datetime
import sys

class TimeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setting the background to be transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")

        self.is_24hr_format = False  # Default is 12-hour format
        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setGeometry(0, 0, 250, 20)  # Set label position and size

        # Setting the font to "Nimbus Sans Bold" and color to white
        self.time_label.setFont(QFont('Impact', 20))
        self.time_label.setStyleSheet("color: white;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1000 ms = 1 second

        self.setGeometry(100, 100, 250, 120)
        self.show()

    def time_text(self):
        if self.is_24hr_format:
            return datetime.now().strftime('%H:%M')
        else:
            return datetime.now().strftime('%I:%M %p')

    def update_time(self):
        current_time = self.time_text()
        self.time_label.setText(current_time)