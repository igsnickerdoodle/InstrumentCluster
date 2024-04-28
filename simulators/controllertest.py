from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QRadialGradient, QBrush
from pathlib import Path
import math, sys

class ControlTest(QWidget):
    def __init__(self, indicator_lights, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Control Test")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: grey;") 
        self.create_toggle_buttons()  # Initialize UI components here
        self.indicator_lights = indicator_lights

    def create_toggle_buttons(self):
         # CEL Button
        self.toggle_button_cel = QPushButton("Toggle CEL", self)
        self.toggle_button_cel.clicked.connect(self.cel)
        self.toggle_button_cel.setGeometry(10, 10, 120, 40)
        self.toggle_button_cel.setStyleSheet("background-color: red")
        self.toggle_button_cel.show()

        # High Beam Button
        self.toggle_button_highbeams = QPushButton("Toggle High Beams", self)
        self.toggle_button_highbeams.clicked.connect(self.highbeams)
        self.toggle_button_highbeams.setGeometry(10, 60, 120, 40)
        self.toggle_button_highbeams.setStyleSheet("background-color: red")
        self.toggle_button_highbeams.show()

        # Fog Lights Button
        self.toggle_button_foglights = QPushButton("Toggle Fog Lights", self)
        self.toggle_button_foglights.clicked.connect(self.foglights)
        self.toggle_button_foglights.setGeometry(10, 110, 120, 40)
        self.toggle_button_foglights.setStyleSheet("background-color: red")
        self.toggle_button_foglights.show()

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
        layout.addWidget(self.toggle_button_cel)
        layout.addWidget(self.toggle_button_foglights)
        layout.addWidget(self.toggle_button_highbeams)
        layout.addWidget(self.rpm_slider_label)  
        layout.addWidget(self.rpm_slider)  
        layout.addWidget(self.speed_slider_label)  
        layout.addWidget(self.speed_slider) 
        layout.addWidget(self.fuel_slider_label) 
        layout.addWidget(self.fuel_slider) 
        layout.addWidget(self.coolant_slider_label)
        layout.addWidget(self.coolant_slider)
        self.setLayout(layout)
        
        # Connector
        # self.rpm_widget = rpm_widget_instance
        # self.speed_widget = speed_widget_instance
        # self.fuel_widget = fuel_widget_instance
        # self.coolant_widget = coolant_widget_instance
        # self.main_display = main_display_instance

    def cel(self):
        self.indicator_lights.cel()  # Call the cel method of IndicatorLights instance

    def highbeams(self):
        self.indicator_lights.highbeams()  # Call the highbeams method

    def foglights(self):
        self.indicator_lights.foglights()  # Call the foglights method

    ## Repaint Methods
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
