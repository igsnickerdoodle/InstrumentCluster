from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout, QSlider, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from pathlib import Path
import sys

current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))
from components.speed.dd_speed_2 import background_speed, speed_widget
from components.rpm.dd_rpm_2 import background_rpm, rpm_widget
from components.fuel.dd_fuel_1 import background_fuel, fuel_widget
from components.coolant_temp.dd_coolant_1 import background_coolant, coolant_temp

class DualDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.STATIC_WIDTH = 1024
        self.STATIC_HEIGHT = 600        
        self.setFixedSize(self.STATIC_WIDTH, self.STATIC_HEIGHT)
        self.setStyleSheet("background-color: black;")
        
        self.right_display = RightDisplay(self)
        self.left_display = LeftDisplay(self)
        self.center_display = CenterDisplay(self)


        # Define and set the widths for each display
        LEFT_WIDTH = 480
        CENTER_WIDTH = 200
        RIGHT_WIDTH = 480

        self.left_display.setFixedSize(LEFT_WIDTH, self.STATIC_HEIGHT)
        self.center_display.setFixedSize(CENTER_WIDTH, self.STATIC_HEIGHT)
        self.right_display.setFixedSize(RIGHT_WIDTH, self.STATIC_HEIGHT)

        # Position the displays based on their widths
        self.left_display.move(-10, 0)
        self.center_display.move(375, 100)
        self.right_display.move(520, 0)

        self.control_test = ControlTest(self.left_display.rpm_widget,self.right_display.speed_widget,self.left_display.fuel_widget,self.right_display.coolant_widget, self)
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
        self.background_rpm = background_rpm()
        self.rpm_widget = rpm_widget()

        self.background_fuel = background_fuel()
        self.fuel_widget = fuel_widget()

        self.setStyleSheet("background-color: transparent;")
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
        self.custom_width = 400
        self.custom_height = 150
        self.setFixedSize(self.custom_width, self.custom_height)
    def paintEvent(self, event):
        painter = QPainter(self)

        # Set the brush for the background
        painter.setBrush(QColor(0, 0, 0))  # Black color
        painter.setPen(QPen(QColor(255, 255, 255), 4))  # White color with 2 pixel width for the border

        # Draw the rectangle with the black background and white border
        painter.drawRect(1, 1, self.custom_width - 2, self.custom_height - 2)

        painter.end()

        
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
class GridWidget(QWidget):
    def __init__(self, grid_pixel_size=10, parent=None):
        super().__init__(parent)
        self.grid_pixel_size = grid_pixel_size
        
        # Set background color to white
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(p)

        # Maximize the widget to fill the screen
        self.showMaximized()

    def set_grid_pixel_size(self, size):
        """Adjust the pixel size of the grid."""
        self.grid_pixel_size = size
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        """Override the paintEvent to draw the grid."""
        painter = QPainter(self)
        painter.setPen(QPen(QColor(220, 220, 220)))  # Gray color for the grid

        # Draw vertical lines
        x = self.grid_pixel_size
        while x < self.width():
            painter.drawLine(x, 0, x, self.height())
            x += self.grid_pixel_size

        # Draw horizontal lines
        y = self.grid_pixel_size
        while y < self.height():
            painter.drawLine(0, y, self.width(), y)
            y += self.grid_pixel_size

        painter.end()

    def resizeEvent(self, event):
        """Override the resizeEvent to redraw the grid when the widget is resized."""
        self.update()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = DualDisplay()
    mainWin.show()
    mainWin.control_test.show()

    sys.exit(app.exec_())
