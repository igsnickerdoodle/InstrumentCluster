from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QTransform, QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from . import update_rpm, Config
import math
from designs.singledial.singledial import Config

class RpmMeter(QWidget):
        def __init__(self, parent=None):
                super().__init__(parent)
                self.config = Config()
                self.rpm = 0

        def RpmNeedle(self, painter):
                pivot_x = 250 + self.config.global_x
                pivot_y = 300 + self.config.global_y
                start_angle = -5
                end_angle = 269
                center_angle = (start_angle + end_angle) / 2
                needle_radius = 260
                angle_range = abs(end_angle - start_angle)
                needle_angle = center_angle + (self.rpm / 8000) * angle_range
                ## RPM needle image import
                pixmap = QPixmap('resources/rpmneedle.png')
                ## Secondary resize on the rpm needle 
                pixmap = pixmap.scaled(QSize(26, 90),Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                # Calculate needle position
                needle_x = pivot_x + needle_radius * math.cos(math.radians(needle_angle)) - pixmap.width() / 2
                needle_y = pivot_y + needle_radius * math.sin(math.radians(needle_angle)) - pixmap.height() / 2
                transform = QTransform()
                transform.translate(needle_x + pixmap.width() / 2, needle_y + pixmap.height() / 2)
                transform.rotate(-270)  # Initial rotation to align with angle = 0 upward.
                transform.rotate(needle_angle)
                transform.translate(-needle_x - pixmap.width() / 2, -needle_y - pixmap.height() / 2)
                # Draw pixmap centered on pivot point
                painter.setTransform(transform)
                painter.drawPixmap(int(needle_x), int(needle_y), pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                # Reset transformation after drawing
                painter.resetTransform()
        def repaint_rpm(self):
            self.update()

        update_rpm = update_rpm
