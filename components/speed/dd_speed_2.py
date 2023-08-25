from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QSlider, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import math, sys

global_x = -30
global_y = 10

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

        self.indicator_xvalue_a = 360 + global_x
        self.indicator_yvalue_a = 290 + global_y

        self.indicator_color = QColor(255, 255, 255)
        self.speed_needle = speed_widget()
        self.slider_controls()
    def paintEvent(self, event):
        painter = QPainter(self)
        # self.draw_grid(painter)
        self.speed_needle.speed_widget(painter)
        self.speed_bg_a(painter)
        self.speed_bg_indicators_c(painter)        
        self.speed_bg_indicators_b(painter)
        self.speed_bg_indicators_a(painter)
        self.speed_bg_text(painter)
        self.speed_bg_b(painter)
    def speed_bg_a(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(76, 76, 76), 15, Qt.SolidLine))
        painter.drawArc(global_x, 0 + global_y, 460, 560, 70 * 16, -135 * 16)
    def speed_bg_b(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(36, 36, 36), 8, Qt.SolidLine))
        painter.drawArc(5 + global_x, -5 + global_y, 460, 570, 72 * 16, -138  * 16)       
    def speed_bg_indicators_a(self, painter):
        start_angle = 58
        end_angle = -63.5
        total_angle_range = end_angle - start_angle
        angle_interval = total_angle_range / 10

        offset_x = -161 + global_x
        offset_y = -12 + global_y

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
        start_angle = 58
        end_angle = -63.5
        total_angle_range = end_angle - start_angle
        num_intervals = 20  
        angle_interval = total_angle_range / num_intervals

        offset_x = -161 + global_x
        offset_y = -12 + global_y

        oblong_ratio = 500 / 520  
        outer_radius_y = 310  
        outer_radius_x = outer_radius_y * oblong_ratio 
        inner_radius_y = outer_radius_y - self.indicator_length_b
        inner_radius_x = outer_radius_x - (self.indicator_length_b * oblong_ratio) 

        painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))

        for i in range(num_intervals + 1):  # +1 to include the 200 Speed indicator
            if i % 20 == 0:  # Skip every 20th including 0
                continue
            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)) + offset_x)
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)) + offset_y)
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)) + offset_x)
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)) + offset_y)
            painter.drawLine(start_x, start_y, end_x, end_y)
    def speed_bg_indicators_c(self, painter):
        # Draw indicator lines
        start_angle = 58
        end_angle = -63.5
        total_angle_range = end_angle - start_angle
        num_intervals = 40
        angle_interval = total_angle_range / num_intervals

        offset_x = -161 + global_x
        offset_y = -12 + global_y

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
        start_angle = 58
        end_angle = -64
        total_angle_range = end_angle - start_angle
        angle_interval = total_angle_range / 10

        vertical_offset = -35 + global_y 
        horizontal_offset = -165 + global_x
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
    def update_speed(self, value):
        self.speed_needle.speed = int(value)
        self.repaint_speed()
    def repaint_speed(self):
        self.repaint()

class speed_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speed = 0
        self.max_speed_value = 200
        self.needle_length = 25
        self.needle_width = 4

    def paintEvent(self, painter):
        painter = QPainter(self)
        self.speed_widget(painter)
    def speed_widget(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        pivot_x = 220 + global_x
        pivot_y = 280 + global_y
        bar_width = 17 
        fill_percentage = self.speed / self.max_speed_value
        radius_x = 460 / 2.1
        radius_y = 560 / 2.1
        ellipse_rect = QtCore.QRectF(pivot_x - radius_x, pivot_y - radius_y, 2 * radius_x, 2 * radius_y)

        start_angle = -64 * 16
        end_angle = 68 * 16  
        span_angle = int(fill_percentage * (end_angle - start_angle))

        # Background arc
        painter.setPen(QPen(QColor(200, 200, 200, 0), bar_width, Qt.SolidLine))  # Made it opaque
        painter.drawArc(ellipse_rect, start_angle, end_angle - start_angle)

        # Foreground arc (showing speed)
        painter.setPen(QPen(QColor(200, 200, 200), bar_width, Qt.SolidLine))
        painter.drawArc(ellipse_rect, start_angle, span_angle)



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
