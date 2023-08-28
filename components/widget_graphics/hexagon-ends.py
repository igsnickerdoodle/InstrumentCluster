from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor
from pathlib import Path
import sys

class hexagon_center_widget(QWidget):
    def __init__(self, parent=None):
           super().__init__(parent)

    def central_widget_bg_a(self, painter):
            painter.setRenderHint(QPainter.Antialiasing)

            painter.setPen(QPen(QColor('white'), 2))
            painter.drawLine(self.x, 0, self.width + self.x, 0)
            painter.drawLine(self.x, self.height, self.width + self.x, self.height)

            # Left half-hexagon (outwards orientation and within boundaries)
            offset = int(self.height / 4)  # Adjusting the offset and converting to int
            painter.drawLine(self.x, 0, -offset + self.x, offset)
            painter.drawLine(-offset + self.x, offset, -offset + self.x, self.height - offset)
            painter.drawLine(-offset + self.x, self.height - offset, self.x, self.height)

            # Right half-hexagon (this remains unchanged)
            painter.drawLine(self.width + self.x, 0, self.width + offset + self.x, offset)
            painter.drawLine(self.width + offset + self.x, offset, self.width + offset + self.x, self.height - offset)
            painter.drawLine(self.width + offset + self.x, self.height - offset, self.width + self.x, self.height)

            painter.end()
    def central_widget_bg_b(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor('white'), 2))
        painter.drawLine(self.x, 0, self.width + self.x, 0)
        painter.drawLine(self.x, self.height, self.width + self.x, self.height)

        # Left half-hexagon (outwards orientation and within boundaries)
        offset = int(self.height / 4)  # Adjusting the offset and converting to int
        painter.drawLine(self.x, 0, -offset + self.x, offset)
        painter.drawLine(-offset + self.x, offset, -offset + self.x, self.height - offset)
        painter.drawLine(-offset + self.x, self.height - offset, self.x, self.height)

        # Right half-hexagon (this remains unchanged)
        painter.drawLine(self.width + self.x, 0, self.width + offset + self.x, offset)
        painter.drawLine(self.width + offset + self.x, offset, self.width + offset + self.x, self.height - offset)
        painter.drawLine(self.width + offset + self.x, self.height - offset, self.width + self.x, self.height) 

        painter.end()  