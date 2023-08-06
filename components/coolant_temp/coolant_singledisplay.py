from PyQt5.QtCore import QPoint, QPointF, QSize
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QFont, QPixmap
from PyQt5.QtWidgets import QWidget
import math

class CoolantGauge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.coolant = 0
        self.coolant_x = 0
        self.coolant_y = 0
    def paintEvent(self, event):
        painter = QPainter(self)
        self.CoolantTemp(painter)
    def CoolantTemp(self, painter):
        start_angle = 62
        end_angle = 118
        major_length = 12
        minor_length = 6
        needle_radius = 300
        major_indicators = {0: major_length, 210: major_length, 420: major_length}
        minor_indicators = {105: minor_length, 315: minor_length}
        text_labels = {0: "C", 420: "H"}
        pivot_x = 265 + self.coolant_x
        pivot_y = 300 + self.coolant_y

        text_radius = 300
        text_angle_offsets = {0:-2.5, 210: -2.5, 420: 2.5}

        # Calculate angle range
        angle_range = end_angle - start_angle

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = ((value - 0) / (420 - 0)) * angle_range  # Rescale to the new range
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
            value_scaled = ((value - 0) / (420 - 0)) * angle_range  # Rescale to the new range
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

        # If temperature is below 210 or above 215, scale normally
        if self.coolant < 210 or self.coolant > 215:
            temp_scaled = ((self.coolant - 0) / (420 - 0)) * angle_range  # Rescale to the new range
        # If temperature is within buffer zone (210 - 215), hold the needle at 210 position
        elif 210 <= self.coolant <= 215:
            temp_scaled = ((210 - 0) / (420 - 0)) * angle_range  # Use the lower limit of the buffer zone to scale
        if self.coolant >= 220:
            # Load the image from resources folder
            image_path = 'resources/coolant_warning_icon.png'  # Replace with the actual image file path
            warning_icon = QPixmap(image_path)
 #           if warning_icon.isNull():
 #              print(f"Warning: Unable to load image at {image_path}")

            # Scale the image
            scaled_size = QSize(25, 25)  # Replace with your desired size
            warning_icon = warning_icon.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Set the position where you want to draw the image
            image_x_position = 442 + self.coolant_x  # Replace with the actual x-coordinate
            image_y_position = 118 + self.coolant_y  # Replace with the actual y-coordinate

            # Draw the image
            painter.drawPixmap(QPoint(image_x_position, image_y_position), warning_icon)

        # Calculate the needle angle
        needle_angle = start_angle + temp_scaled

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
    def update_coolant(self, value):
        # Update the Coolant value 
        self.coolant = int(value)
        self.repaint_coolant() 
    def repaint_coolant(self):
        self.update()
