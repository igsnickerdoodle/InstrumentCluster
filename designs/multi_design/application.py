from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from pathlib import Path
import sys

### Local component imports
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))
from components.speed.dd_speed_1 import background_speed, speed_widget
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
        
        self.right_display= RightDisplay(self)
        self.left_display = LeftDisplay(self)
        
        # Setting size policies
        self.right_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Setting up layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.left_display)
        layout.addWidget(self.right_display)
        self.setLayout(layout)
        self.control_test = ControlTest(self.left_display.rpm_widget,self.right_display.speed_widget,self.left_display.fuel_widget,self.right_display.coolant_widget, self)
    def toggle_grid(self):
        """Toggle the visibility of the grid."""
        self.show_grid = not self.show_grid
        self.update()  # Trigger a repaint

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
        self.background_speed.speed_bg_a(painter)
        self.background_speed.speed_bg_indicators_a(painter)
        self.background_speed.speed_bg_indicators_b(painter)
        self.background_speed.speed_bg_indicators_c(painter)
        self.background_speed.speed_bg_text(painter)
        self.background_speed.speed_bg_b(painter)
        self.speed_widget.speed_needle(painter)
        ## Paint Coolant
        self.coolant_widget.bar_widget(painter)
               
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
