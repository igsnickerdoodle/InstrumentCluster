from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QSlider, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import math, sys


class background_rpm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rpm = 0
        self.max_rpm_value = 8000
        self.needle_length = 25
        self.needle_width = 4

        self.indicator_length_a = 20
        self.indicator_length_b = 13
        self.indicator_length_c = 6

        self.indicator_xvalue_a = 375
        self.indicator_yvalue_a = 290

        self.rpm_font_size = 12

        self.dynamic_redline = 6000

        self.indicator_color = QColor(255, 255, 255)
        self.rpm_needle = rpm_widget()
        self.slider_controls()
    def paintEvent(self, event):
        painter = QPainter(self)
        self.rpm_bg_a(painter)
        self.rpm_needle.bar_widget(painter)        
        self.rpm_bg_indicators_c(painter)        
        self.rpm_bg_indicators_b(painter)
        self.rpm_bg_indicators_a(painter)
        self.rpm_bg_b(painter)
        self.rpm_bg_text(painter)
    def rpm_bg_a(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(76, 76, 76), 15, Qt.SolidLine))
        painter.drawArc(72, 10, 460, 560, 115 * 16, 135 * 16)
    def rpm_bg_b(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(36, 36, 36), 8, Qt.SolidLine))
        painter.drawArc(69, 5, 460, 570, 115 * 16, 135 * 16)        
    def rpm_bg_indicators_a(self, painter):
        start_angle = 119
        end_angle = 237
        total_angle_range = end_angle - start_angle
        angle_interval = total_angle_range / 8

        oblong_ratio = 500 / 510  
        outer_radius_y = 310  
        outer_radius_x = outer_radius_y * oblong_ratio 
        inner_radius_y = outer_radius_y - self.indicator_length_a
        inner_radius_x = outer_radius_x - (self.indicator_length_a * oblong_ratio) 

        redline_indicator = int(math.ceil(self.dynamic_redline / 1000.0))

        for i in range(9):
            if i >= redline_indicator:
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))
            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)))
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)))
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)))
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)))
            painter.drawLine(start_x, start_y, end_x, end_y)
    def rpm_bg_indicators_b(self, painter):
        start_angle = 119
        end_angle = 237
        total_angle_range = end_angle - start_angle
        num_intervals = 16  # For 0 to 8000 RPM in 500 RPM steps
        angle_interval = total_angle_range / num_intervals

        oblong_ratio = 500 / 510  
        outer_radius_y = 310  
        outer_radius_x = outer_radius_y * oblong_ratio 
        inner_radius_y = outer_radius_y - self.indicator_length_b
        inner_radius_x = outer_radius_x - (self.indicator_length_b * oblong_ratio) 

        # Determine the indicator number from which the color should be red
        redline_indicator = int(math.ceil(self.dynamic_redline / 500.0))

        for i in range(num_intervals + 1):  # +1 to include the 8000 RPM indicator
            if i >= redline_indicator:
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))
            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)))
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)))
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)))
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)))
            painter.drawLine(start_x, start_y, end_x, end_y)
    def rpm_bg_indicators_c(self, painter):
        # Draw indicator lines
        start_angle = 119
        end_angle = 237
        total_angle_range = end_angle - start_angle
        num_intervals = 80
        angle_interval = total_angle_range / num_intervals
        oblong_ratio = 500 / 510  # width/height ratio of the oblong shape
        outer_radius_y = 310  
        outer_radius_x = outer_radius_y * oblong_ratio  
        inner_radius_y = outer_radius_y - self.indicator_length_c
        inner_radius_x = outer_radius_x - (self.indicator_length_c * oblong_ratio)  

        # Determine the indicator number from which the color should be red
        redline_indicator = int(math.ceil(self.dynamic_redline / 100.0))
        for i in range(num_intervals + 1):  # +1 to include the last indicator
            self.max_rpm_value = i * 100
            if self.max_rpm_value % 500 == 0:  # Check if it's a multiple of 500
                continue 
            if i >= redline_indicator:
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.indicator_color, 2, Qt.SolidLine))

            angle = start_angle + i * angle_interval
            start_x = int(self.indicator_xvalue_a + inner_radius_x * math.cos(math.radians(angle)))
            start_y = int(self.indicator_yvalue_a + inner_radius_y * math.sin(math.radians(angle)))
            end_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)))
            end_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)))

            painter.drawLine(start_x, start_y, end_x, end_y)
    def rpm_bg_text(self, painter):
        start_angle = 119
        end_angle = 236
        total_angle_range = end_angle - start_angle
        angle_interval = total_angle_range / 8
        offset_x = 0
        offset_y = 5
        oblong_ratio = 500 / 510  
        outer_radius_y = 280  
        outer_radius_x = outer_radius_y * oblong_ratio 
        font = painter.font()
        font.setPointSize(self.rpm_font_size)
        painter.setFont(font)
        painter.setPen(self.indicator_color)
        for i in range(9):
            angle = start_angle + i * angle_interval
            text_x = int(self.indicator_xvalue_a + outer_radius_x * math.cos(math.radians(angle)) + offset_x)
            text_y = int(self.indicator_yvalue_a + outer_radius_y * math.sin(math.radians(angle)) + offset_y)
            painter.drawText(text_x, text_y, str(i))
    def slider_controls(self):
        main_layout = QVBoxLayout(self)
        
        # Spacer to push the slider to the bottom
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        
        # Create a slider with a range from 0 to 8000
        self.rpm_slider = QSlider(Qt.Horizontal)
        self.rpm_slider.setRange(0, 8000)
        self.rpm_slider.valueChanged.connect(self.update_rpm)
        self.rpm_slider.setStyleSheet("background-color: white;")
        
        main_layout.addWidget(self.rpm_slider)
        main_layout.addWidget(self.rpm_needle)
        self.setLayout(main_layout)
    def update_rpm(self, value):
        self.rpm_needle.rpm = int(value)
        self.repaint_rpm()
    def repaint_rpm(self):
        self.repaint()
class rpm_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rpm = 0
        self.max_rpm_value = 8000
        self.needle_length = 25
        self.needle_width = 4
    def paintEvent(self, event):
        painter = QPainter(self)
        self.bar_widget(painter)
    def bar_widget(self, painter):
        pivot_x = 375
        pivot_y = 290
        bar_width = 17 
        bar_height = 300
        fill_percentage = self.rpm / self.max_rpm_value
        ellipse_rect = QtCore.QRectF(pivot_x - bar_height, pivot_y - bar_height, 2 * bar_height, 2 * bar_height)
        start_angle = 240 * 16
        end_angle = 124 * 16  
        span_angle = int(fill_percentage * (end_angle - start_angle)) 
        painter.setPen(QPen(QColor(200, 200, 200, 0), bar_width, Qt.SolidLine))
        painter.drawArc(ellipse_rect, start_angle, end_angle - start_angle)
        painter.setPen(QPen(QColor(130, 180, 187), bar_width, Qt.SolidLine))
        painter.drawArc(ellipse_rect, start_angle, span_angle)
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create and set the rpm_display widget as the central widget
        self.rpm_widget = background_rpm(self)
        self.setCentralWidget(self.rpm_widget)

        # Set the background color to black
        self.setStyleSheet("background-color: black;")
        
        # Set the window size to 1024x600
        self.resize(1024, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())