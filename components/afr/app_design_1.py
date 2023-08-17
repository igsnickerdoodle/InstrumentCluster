from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QFont
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
import math, sys

from pathlib import Path
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))
from components.afr import update_afr, global_x, global_y, text_labels


class afr_display(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.afr_value = 14.7
        self.coolant_x = 0
        self.coolant_y = 0
        self.global_x = global_x
        self.global_y = global_y
        self.text_labels = "Nimbus Sans Bold", 8

    def widget(self, painter):
        start_angle = -45
        end_angle = 45
        major_length = 10
        minor_length = 3
        needle_radius = 218
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "Rich", 100: "Lean"}
        pivot_x = 250 + self.global_x
        pivot_y = 300 + self.global_y
        text_radius = 195
        text_angle_offsets = {0: 0, 0: 0, 0: 0}
        # Calculate angle range
        angle_range = end_angle - start_angle

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))
            # Draw the text labels
            if value in text_labels:
                text_angle = indicator_angle + text_angle_offsets.get(value, 0)
                text_x = pivot_x + text_radius * math.cos(math.radians(90 - text_angle))
                text_y = pivot_y + text_radius * math.sin(math.radians(90 - text_angle))
                font = QFont("Nimbus Sans", 8)
                painter.setFont(font)
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPointF(text_x, text_y), text_labels[value])
            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 4)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)
        # Draw the minor indicators
        for value, length in minor_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 2)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        afr_value_scaled = ((self.afr_value - 8.5) / (18 - 8.5)) * angle_range
        # Calculate the needle angle
        needle_angle = start_angle + afr_value_scaled

        # Compute the start and end points of the needle
        start_x = pivot_x + needle_radius * math.cos(math.radians(90 - needle_angle))
        start_y = pivot_y + needle_radius * math.sin(math.radians(90 - needle_angle))
        end_x = pivot_x + (needle_radius - 10) * math.cos(math.radians(90 - needle_angle))
        end_y = pivot_y + (needle_radius - 10) * math.sin(math.radians(90 - needle_angle))
        path = QPainterPath()
        path.moveTo(start_x, start_y)
        path.lineTo(end_x, end_y)
        pen = QPen(Qt.red, 4)

        painter.setPen(pen)
        painter.drawPath(path)

        # Position of the text field
        text_field_x = pivot_x  + -10 # Adjust these values as desired
        text_field_y = pivot_y + 200  # Adjust these values as desired


        font = QFont("Nimbus Sans", 10)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))
        painter.drawText(QPointF(text_field_x, text_field_y), str(self.afr_value))

    def repaint_afr(self):
        self.update()
    
    update_afr = update_afr