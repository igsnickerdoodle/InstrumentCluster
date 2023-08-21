from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QSlider, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import math, sys


class background_speed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speed = 0
        self.max_speed_value = 210
        self.needle_length = 25
        self.needle_width = 4

        self.indicator_length_a = 20
        self.indicator_length_b = 13
        self.indicator_length_c = 6

        self.indicator_xvalue_a = 330
        self.indicator_yvalue_a = 290

        self.indicator_color = QColor(255, 255, 255)
        self.speed_needle = speed_widget()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.speed_bg_a(painter)
        self.speed_bg_indicators_c(painter)        
        self.speed_bg_indicators_b(painter)
        self.speed_bg_indicators_a(painter)
        self.speed_bg_text(painter)
        self.speed_bg_b(painter)
        self.speed_needle.speed_needle(painter)

    def speed_bg_a(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(76, 76, 76), 15, Qt.SolidLine))
        painter.drawArc(0, 10, 460, 560, 70 * 16, -135 * 16)
    def speed_bg_b(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(36, 36, 36), 8, Qt.SolidLine))
        painter.drawArc(5, 5, 460, 570, 72 * 16, -139  * 16)       
    def speed_bg_indicators_a(self, painter):
        start_angle = 59
        end_angle = -63
        total_angle_range = end_angle - start_angle
        angle_interval = total_angle_range / 10

        offset_x = -161
        offset_y = 0

        oblong_ratio = 500 / 520  
        outer_radius_y = 310  
        outer_radius_x = outer_radius_y * oblong_ratio 
        inner_radius_y = outer_radius_y - self.indicator_length_a
        inner_radius_x = outer_radius_x - (self.indicator_length_a * oblong_ratio) 

        painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))

        for i in range(11):
            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)) + offset_x)
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)) + offset_y)
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)) + offset_x)
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)) + offset_y)
            painter.drawLine(start_x, start_y, end_x, end_y)
    def speed_bg_indicators_b(self, painter):
        start_angle = 59
        end_angle = -63
        total_angle_range = end_angle - start_angle
        num_intervals = 20  
        angle_interval = total_angle_range / num_intervals

        offset_x = -161
        offset_y = 0

        oblong_ratio = 500 / 520  
        outer_radius_y = 310  
        outer_radius_x = outer_radius_y * oblong_ratio 
        inner_radius_y = outer_radius_y - self.indicator_length_b
        inner_radius_x = outer_radius_x - (self.indicator_length_b * oblong_ratio) 

        painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))

        for i in range(num_intervals + 1):  # +1 to include the 200 Speed indicator
            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)) + offset_x)
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)) + offset_y)
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)) + offset_x)
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)) + offset_y)
            painter.drawLine(start_x, start_y, end_x, end_y)
    def speed_bg_indicators_c(self, painter):
        # Draw indicator lines
        start_angle = 59
        end_angle = -63
        total_angle_range = end_angle - start_angle
        num_intervals = 40
        angle_interval = total_angle_range / num_intervals

        offset_x = -161
        offset_y = 0

        oblong_ratio = 500 / 520  # width/height ratio of the oblong shape
        outer_radius_y = 305  
        outer_radius_x = outer_radius_y * oblong_ratio  
        inner_radius_y = outer_radius_y - self.indicator_length_c
        inner_radius_x = outer_radius_x - (self.indicator_length_c * oblong_ratio)  

        painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))

        for i in range(num_intervals + 1):
            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)) + offset_x)
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)) + offset_y)
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)) + offset_x)
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)) + offset_y)

            painter.drawLine(start_x, start_y, end_x, end_y)
    def speed_bg_text(self, painter):
        start_angle = 59
        end_angle = -63
        total_angle_range = end_angle - start_angle
        angle_interval = total_angle_range / 10

        vertical_offset = -35  
        horizontal_offset = -170
        oblong_ratio = 500 / 550  
        outer_radius_y = 275 
        outer_radius_x = outer_radius_y * oblong_ratio 

        # Set the font and color for the text
        font = painter.font()
        font.setPointSize(12)  # Adjust the font size as needed
        painter.setFont(font)
        painter.setPen(self.indicator_color)

        for i in range(11):
            angle = start_angle + i * angle_interval
            text_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle))) + horizontal_offset
            text_y = int(self.indicator_xvalue_a + outer_radius_y * math.sin(math.radians(angle))) + vertical_offset
            
            painter.drawText(text_x, text_y, str(i*20))


class speed_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speed = 0
        self.max_speed_value = 210
        self.needle_length = 25
        self.needle_width = 4
        # self.slider_controls()
    def paintEvent(self, painter):
        painter = QPainter(self)
        self.speed_needle(painter)
    def speed_needle(self, painter):
        pivot_x = 140
        pivot_y = 290
        start_angle = 56 
        end_angle = -65.5 
        angle_range = end_angle - start_angle
        radius_offset_y = 20       
        radius_offset_x = 22

        speed_per_degree = self.max_speed_value / angle_range
        needle_angle = start_angle + (self.speed / speed_per_degree)
        needle_tip_x = int(pivot_x + (300 + radius_offset_x) * math.cos(math.radians(needle_angle)))  
        needle_tip_y = int(pivot_y + (300 + radius_offset_y) * math.sin(math.radians(needle_angle)))     
        needle_base_x = int(pivot_x + (300 - self.needle_length + radius_offset_x) * math.cos(math.radians(needle_angle)))
        needle_base_y = int(pivot_y + (300 - self.needle_length + radius_offset_y) * math.sin(math.radians(needle_angle)))
        painter.setPen(QPen(QColor(255, 0, 0), self.needle_width, Qt.SolidLine))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawLine(needle_base_x, needle_base_y, needle_tip_x, needle_tip_y)
    def update_speed(self, value):
        self.speed = int(value)
        self.repaint_speed()
    def repaint_speed(self):
        self.update()

    def slider_controls(self):
        main_layout = QVBoxLayout(self)
        
        # Spacer to push the slider to the bottom
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        
        # Create a slider with a range from 0 to 200
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(0, 200)
        self.speed_slider.valueChanged.connect(self.update_speed)
        self.speed_slider.setStyleSheet("background-color: white;")
        
        main_layout.addWidget(self.speed_slider)
        self.setLayout(main_layout)
  

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create and set the speed_display widget as the central widget
        self.speed_widget = background_speed(self)
        self.setCentralWidget(self.speed_widget)

        # Set the background color to black
        self.setStyleSheet("background-color: black;")
        
        # Set the window size to 1024x600
        self.resize(1024, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
