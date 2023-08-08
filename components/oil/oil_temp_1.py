from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QPen, QFont, QPainterPath, QFontMetrics
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
import math

from designs.singledial.singledial import Config
from . import update_oil_temp, Config


class OilMeter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_labels = self.config.text_labels
        self.needle_color = Qt.red
        self.needle_size = 4
        self.config = Config()
        self.oil_temp = 0

    def needle(self, painter, *args, **kwargs):
            start_angle = 230
            end_angle = 132
            major_length = 12
            minor_length = 6
            needle_radius = 218
            major_indicators = {0: major_length, 50: major_length, 100: major_length}
            minor_indicators = {25: minor_length, 75: minor_length}
            text_labels = {0: "C", 100: "H"}
            pivot_x = 250 + self.config.global_x
            pivot_y = 295 + self.config.global_y
            text_radius = 200
            text_angle_offsets = {0: 1, 50: -2.5, 100: -3}

            angle_range = end_angle - start_angle

            # Draw line indicators
            # Draw major indicators
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
            # Draw minor indicators
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

            oil_temp = (self.oil_temp / 260) * 260

            # Scale the oil temperature to the range of the start and end angles
            scaled_oil_temp = ((oil_temp - 0) / (260 - 0)) * (end_angle - start_angle)
            needle_angle = start_angle + scaled_oil_temp
            
            # Calculate the start and end points of the needle
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
            pivot_x_offset = 0  # Adjust this value as desired
            text_field_x = pivot_x + pivot_x_offset
            text_field_y = pivot_y + self.config.global_y - 240

            # Draw the text field with the current value
            oiltemp_font = QFont("Nimbus Sans Bold", 10) 
            painter.setFont(oiltemp_font)
            painter.setPen(QPen(Qt.white))  # Adjust color as needed

            ## Display OilTemp in Text 
            text = str(round(((self.oil_temp / 260) * 260))) + 'C'
            # Calculate the text width
            metrics = QFontMetrics(font)
            width = metrics.width(text)
            text_field_x_adjusted = text_field_x - width / 2  
            # Draw the text
            painter.drawText(QPointF(text_field_x_adjusted, text_field_y), text)
    
    def repaint_oil_temp(self):
        self.update()
    update_oil_temp = update_oil_temp