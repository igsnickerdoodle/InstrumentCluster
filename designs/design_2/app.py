from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
from datetime import time
from pathlib import Path
import sys

current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))

from InstrumentCluster.components.speed.dd2 import background_speed, speed_widget
from components.rpm.dd_rpm_2 import background_rpm, rpm_widget
from components.fuel.dd_fuel_1 import background_fuel, fuel_widget
from components.coolant_temp.dd_coolant_1 import background_coolant, coolant_temp
from components.time.dd_time_display import TimeWidget

class instrumentcluster(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.STATIC_WIDTH = 1024
        self.STATIC_HEIGHT = 600        
        self.setFixedSize(self.STATIC_WIDTH, self.STATIC_HEIGHT)
        self.setStyleSheet("background-color: black;")     
        self.right_display = RightDisplay(self)
        self.left_display = LeftDisplay(self)
        self.central_display = CenterDisplay(self)
        LEFT_WIDTH = 580
        CENTER_WIDTH = 1024
        RIGHT_WIDTH = 580
        self.left_display.setFixedSize(LEFT_WIDTH, self.STATIC_HEIGHT)
        self.central_display.setFixedSize(CENTER_WIDTH, self.STATIC_HEIGHT)
        self.right_display.setFixedSize(RIGHT_WIDTH, self.STATIC_HEIGHT)

        self.left_display.move(-10, 0)
        self.central_display.move(85, -25)
        self.right_display.move(531, 0)

        self.control_test = ControlTest(self.left_display.rpm_widget,
                                        self.right_display.speed_widget,
                                        self.left_display.fuel_widget,
                                        self.right_display.coolant_widget,
                                        self)
    def paintEvent(self, event):
        painter = QPainter(self)
        # self.draw_grid(painter)
    def draw_grid(self, painter):
        width = self.width()
        height = self.height()

        # Grid settings
        grid_color = QColor(100, 100, 100)  # Light gray for grid
        grid_spacing = 10  # Spacing for the 5x5 grid

        # Set pen for the grid
        painter.setPen(QPen(grid_color, 1, Qt.SolidLine))

        # Draw vertical lines
        for x in range(0, width, grid_spacing):
            painter.drawLine(x, 0, x, height)

        # Draw horizontal lines
        for y in range(0, height, grid_spacing):
            painter.drawLine(0, y, width, y)
        painter.end()   

class RightDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")        
        self.background_speed = background_speed()
        self.speed_widget = speed_widget()
        self.background_coolant = background_coolant()
        self.coolant_widget = coolant_temp()
    def paintEvent(self, event):
        painter = QPainter(self)

        ## Paint Speedometer
        self.speed_widget.bar_widget(painter)
        self.speed_widget.text_widget(painter)
        self.background_speed.speed_bg_a(painter)
        self.background_speed.speed_bg_indicators_a(painter)
        self.background_speed.speed_bg_indicators_b(painter)
        self.background_speed.speed_bg_indicators_c(painter)
        self.background_speed.speed_bg_text(painter)
        self.background_speed.speed_bg_b(painter)

        ## Paint Coolant
        self.coolant_widget.bar_widget(painter)
        self.background_coolant.coolant_indicators(painter)

class LeftDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.background_rpm = background_rpm()
        self.rpm_widget = rpm_widget()
        self.background_fuel = background_fuel()
        self.fuel_widget = fuel_widget()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        self.background_rpm.rpm_bg_a(painter)
        self.rpm_widget.bar_widget(painter)
        self.background_rpm.rpm_bg_indicators_a(painter)
        self.background_rpm.rpm_bg_indicators_b(painter)
        self.background_rpm.rpm_bg_indicators_c(painter)
        self.background_rpm.rpm_bg_text(painter)
        self.background_rpm.rpm_bg_b(painter) 

        self.background_fuel.fuel_indicators(painter)
        self.fuel_widget.bar_widget(painter)       

class CenterDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        self.x = 300
        self.y = 50
        self.width = 250
        self.height = 520

        self.time = TimeWidget(self)
        self.time.move(self.x, self.y + 30)
    def paintEvent(self, event):
        painter = QPainter(self)
        self.central_widget_lines(painter)        
        self.central_widget_bg_a(painter)
        # self.central_widget_bg_b(painter)

    def central_widget_bg_a(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        main_color = QColor('#353535')     
        highlight_color = QColor('#4B4B4B')   
        shadow_color = QColor('#282828')   
        line_thickness = 4

        # Top
        painter.setPen(QPen(highlight_color, line_thickness))
        painter.drawLine(self.x, self.y - 4, self.x + self.width, self.y - 4)
        painter.setPen(QPen(main_color, line_thickness))
        painter.drawLine(self.x, self.y, self.x + self.width, self.y)
        painter.setPen(QPen(shadow_color, line_thickness))
        painter.drawLine(self.x, self.y + 4, self.x + self.width, self.y + 4)
        # Bottom 
        painter.setPen(QPen(highlight_color, line_thickness))
        painter.drawLine(self.x, self.y + self.height - 4, self.x + self.width, self.y + self.height - 4)
        painter.setPen(QPen(main_color, line_thickness))
        painter.drawLine(self.x, self.y + self.height, self.x + self.width, self.y + self.height)
        painter.setPen(QPen(shadow_color, line_thickness))
        painter.drawLine(self.x, self.y + self.height + 4, self.x + self.width, self.y + self.height + 4)
        # Left
        painter.setPen(QPen(highlight_color, line_thickness))
        left_arc_rect_highlight = QRectF(-250 + self.x, self.y - 4, self.height, self.height)
        painter.drawArc(left_arc_rect_highlight, 90 * 16, 180 * 16)
        painter.setPen(QPen(main_color, line_thickness))
        left_arc_rect = QRectF(-250 + self.x, self.y, self.height, self.height)
        painter.drawArc(left_arc_rect, 90 * 16, 180 * 16)
        painter.setPen(QPen(shadow_color, line_thickness))
        left_arc_rect_shadow = QRectF(-250 + self.x, self.y + 4, self.height, self.height)
        painter.drawArc(left_arc_rect_shadow, 90 * 16, 180 * 16)

        # Right 
        painter.setPen(QPen(highlight_color, line_thickness))
        right_arc_rect_highlight = QRectF(250 + self.x + self.width - self.height, self.y - 4, self.height, self.height)
        painter.drawArc(right_arc_rect_highlight, -90 * 16, 180 * 16)
        painter.setPen(QPen(main_color, line_thickness))
        right_arc_rect = QRectF(250 + self.x + self.width - self.height, self.y, self.height, self.height)
        painter.drawArc(right_arc_rect, -90 * 16, 180 * 16)
        painter.setPen(QPen(shadow_color, line_thickness))
        right_arc_rect_shadow = QRectF(250 + self.x + self.width - self.height, self.y + 4, self.height, self.height)
        painter.drawArc(right_arc_rect_shadow, -90 * 16, 180 * 16)
    def central_widget_bg_b(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)  
        # Top/Bottom Lines  
        painter.setPen(QPen(QColor('#838383'), 2))
        painter.drawLine(self.x, self.y, 
                         self.x + self.width, self.y)
        painter.setPen(QPen(QColor('#838383'), 2))
        painter.drawLine(self.x, self.y + self.height, 
                         self.x + self.width, self.y + self.height)
        ## End Capsules
        painter.setPen(QPen(QColor('#838383'), 2))
        left_arc_rect = QRectF(-250 + self.x, self.y, 
                               self.height, self.height)
        painter.drawArc(left_arc_rect, 90 * 16, 180 * 16)
        right_arc_rect = QRectF(250 + self.x + self.width - self.height, 
                                self.y, self.height, self.height)
        painter.drawArc(right_arc_rect, -90 * 16, 180 * 16)  
    def central_widget_lines(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)

        main_color = QColor('#353535')
        highlight_color = QColor('#4B4B4B')
        shadow_color = QColor('#282828')
        line_thickness = 4
        
        # Configuration for Line Top
        line_a_length = 590  
        line_a_x_position = 130     
        line_a_y_position = 125   
        painter.setPen(QPen(highlight_color, line_thickness))
        painter.drawLine(line_a_x_position, line_a_y_position - 2, line_a_x_position + line_a_length, line_a_y_position - 2)
        painter.setPen(QPen(main_color, line_thickness))
        painter.drawLine(line_a_x_position, line_a_y_position, line_a_x_position + line_a_length, line_a_y_position)
        painter.setPen(QPen(shadow_color, line_thickness))
        painter.drawLine(line_a_x_position, line_a_y_position + 2, line_a_x_position + line_a_length, line_a_y_position + 2)

        # Configuration for Line Bottom
        line_b_length = 590
        line_b_x_position = 130
        line_b_y_position = 495
        painter.setPen(QPen(highlight_color, line_thickness))
        painter.drawLine(line_b_x_position, line_b_y_position - 2, line_b_x_position + line_b_length, line_b_y_position - 2)
        painter.setPen(QPen(main_color, line_thickness))
        painter.drawLine(line_b_x_position, line_b_y_position, line_b_x_position + line_b_length, line_b_y_position)
        painter.setPen(QPen(shadow_color, line_thickness))
        painter.drawLine(line_b_x_position, line_b_y_position + 2, line_b_x_position + line_b_length, line_b_y_position + 2)

class ControlTest(QWidget):
    def __init__(self, rpm_widget_instance, speed_widget_instance, fuel_widget_instance, coolant_widget_instance, main_display_instance, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Slider Controls")
        self.setGeometry(100, 100, 300, 200)  

        # RPM Slider configurations
        self.rpm_slider = QSlider(Qt.Horizontal, self)
        self.rpm_slider.setRange(0, 8000) 
        self.rpm_slider_label = QLabel("Rpm", self) 
        self.rpm_slider.valueChanged.connect(self.update_rpm)

        # Speed Slider configurations
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setRange(0, 200) 
        self.speed_slider_label = QLabel("Speed", self)  
        self.speed_slider.valueChanged.connect(self.update_speed)

        # Fuel Slider configurations
        self.fuel_slider = QSlider(Qt.Horizontal, self)
        self.fuel_slider.setRange(0, 100) 
        self.fuel_slider_label = QLabel("Fuel", self)  
        self.fuel_slider.valueChanged.connect(self.update_fuel)
        
        # Coolant Slider configurations
        self.coolant_slider = QSlider(Qt.Horizontal, self)
        self.coolant_slider.setRange(0, 320)  
        self.coolant_slider_label = QLabel("Coolant", self) 
        self.coolant_slider.valueChanged.connect(self.update_coolant)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.rpm_slider_label)  
        layout.addWidget(self.rpm_slider)  
        layout.addWidget(self.speed_slider_label)  
        layout.addWidget(self.speed_slider) 
        layout.addWidget(self.fuel_slider_label) 
        layout.addWidget(self.fuel_slider) 
        layout.addWidget(self.coolant_slider_label)
        layout.addWidget(self.coolant_slider)
        self.setLayout(layout)


        self.rpm_widget = rpm_widget_instance
        self.speed_widget = speed_widget_instance
        self.fuel_widget = fuel_widget_instance
        self.coolant_widget = coolant_widget_instance
        self.main_display = main_display_instance    
    def update_rpm(self, value):
        # print(f"Updating RPM to {value}")
        self.rpm_widget.rpm = int(value)
        self.repaint_rpm()
    def repaint_rpm(self):
        self.main_display.repaint()        
    def update_speed(self, value):
        # print(f"Updating Speed to {value}")
        self.speed_widget.speed = int(value)
        self.repaint_speed()
    def repaint_speed(self):
        self.main_display.repaint()
    def update_fuel(self, value):
        # print(f"Updating Speed to {value}")
        self.fuel_widget.fuel = int(value)
        self.repaint_fuel()
    def repaint_fuel(self):
        self.main_display.repaint()        
    def update_coolant(self, value):
        self.coolant_widget.coolant = int(value)
        self.repaint_coolant()
    def repaint_coolant(self):
        self.main_display.repaint()
        """Override the resizeEvent to redraw the grid when the widget is resized."""
        self.update()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = instrumentcluster()
    mainWin.show()
    mainWin.control_test.show()

    sys.exit(app.exec_())
 