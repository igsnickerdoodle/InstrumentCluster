from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QSlider, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import math, sys

class background_coolant(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fuel = 0
        self.fuel_value = coolant_temp()
        self.slider_controls()
    def paintEvent(self, painter):
        painter = QPainter(self)
        self.fuel_indicators(painter)
        self.fuel_value.bar_widget(painter)  

    def fuel_indicators(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)

        # Define ellipse parameters to match fuel_bg_a and bar_widget
        x, y, width, height = 55, 20, 460, 560
        start_angle = 195 * 16
        total_angle = 55 * 16
        
        # Calculate the angles for each fuel level
        angles = {
            100: start_angle,
            75: start_angle + 0.25 * total_angle,
            50: start_angle + 0.5 * total_angle,
            25: start_angle + 0.75 * total_angle,
            0: start_angle + total_angle
        }

        # Indicator data for each fuel level
        indicators_data = {
            100: {"offset_x": -30, "offset_y": 10, "color": "white", "length": 25},
            75: {"offset_x": -30, "offset_y": 10, "color": "white", "length": 22},
            50: {"offset_x": -28, "offset_y": 10, "color": "white", "length": 22},
            25: {"offset_x": -28, "offset_y": 8, "color": "white", "length": 22},
            0: {"offset_x": -40, "offset_y": 5, "color": "red", "length": 30}
        }

        for level, data in indicators_data.items():
            angle_rad = math.radians(360 - (angles[level] / 16))  # Convert Qt's angle to radians
            
            # Calculate the start point of the indicator line
            start_x = int(x + (width / 2) + (width / 2) * math.cos(angle_rad))
            start_y = int(y + (height / 2) + (height / 2) * math.sin(angle_rad))
            
            # Calculate the end point by simply adding the length to the x-coordinate (for horizontal line)
            end_x = start_x + data['length']
            end_y = start_y
            
            # Apply offsets
            start_x += data['offset_x']
            start_y += data['offset_y']
            end_x += data['offset_x']
            end_y += data['offset_y']

            painter.setPen(QPen(QColor(data['color']), 3, Qt.SolidLine))
            painter.drawLine(start_x, start_y, end_x, end_y)
    def slider_controls(self):
        main_layout = QVBoxLayout(self)
        
        # Spacer to push the slider to the bottom
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        
        # Create a slider with a range from 0 to 100
        self.fuel_slider = QSlider(Qt.Horizontal)
        self.fuel_slider.setRange(0, 100)
        self.fuel_slider.valueChanged.connect(self.update_fuel)
        self.fuel_slider.setStyleSheet("background-color: white;")
        
        main_layout.addWidget(self.fuel_slider)
        main_layout.addWidget(self.fuel_value)

        self.setLayout(main_layout)
    def update_fuel(self, value):
        self.fuel_value.fuel = int(value)
        self.repaint_fuel()
    def repaint_fuel(self):
        self.update()
class coolant_temp(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.fuel = 0
        self.max_fuel_value = 100 
    def bar_widget(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        x, y, width, height = 55, 20, 460, 560
        start_angle = 250 * 16
        total_angle = -55 * 16
        num_segments = 20
        segment_angle = total_angle // num_segments  # adjusted segment angle

        # Draw the background arc (grayed out portion)
        painter.setPen(QPen(QColor(200, 200, 200, 0), 5, Qt.SolidLine))
        painter.drawArc(x, y, width, height, start_angle, total_angle)

        # Calculate the number of filled segments based on the fuel level
        filled_segments = int((self.fuel / 100) * 10) * 2  # Multiply by 2 to account for transparent segments

        current_angle = start_angle
        for i in range(filled_segments):
            # Determine if the segment should be colored or transparent
            is_colored = i % 2 == 0

            if is_colored:
                segment_value = (i // 2 + 1) * 10  # This gives the fuel value represented by the current segment/block
                if segment_value <= 30:
                    painter.setPen(QPen(QColor(255, 0, 0), 5, Qt.SolidLine))  # Red
                else:
                    painter.setPen(QPen(QColor(255, 255, 255), 5, Qt.SolidLine))
            else:
                painter.setPen(QPen(QColor(0, 0, 0, 0), 2, Qt.SolidLine))  # Transparent segment

            painter.drawArc(x, y, width, height, current_angle, segment_angle)
            current_angle += segment_angle
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = background_coolant()
    mainWin.resize(1024, 600) 
    mainWin.setStyleSheet("background-color: black;") 
    mainWin.show()
    sys.exit(app.exec_())