from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QPointF, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QRadialGradient, QBrush
from pathlib import Path
import sys, serial

### Local component imports
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))

from components.rpm.sd_rpm_1 import rpm_display
from components.speed.sd_speed_1 import speed_display 
from components.afr.sd_afr_1 import afr_display
from components.boost.sd_boost_1 import boost_display
from components.fuel.sd_fuel_1 import fuel_display
from components.oil.sd_oil_1 import oil_display
from components.coolant_temp.sd_coolant_1 import coolant_display
from components.indicators.app import IndicatorLights

class Background(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ## Initialize Modules
        self.global_x = 280
        self.global_y = 50
        self.text_labels = "Nimbus Sans Bold"
        
    def top_center_bg(self, painter):
        boostbg_x = 35
        boostbg_y = 85
        boostbg_size = 430
        shadowColor = QColor(8, 8, 8, 128)
        shadowOffset = 2
        painter.setPen(QPen(shadowColor, 20, Qt.SolidLine))
        painter.drawArc(boostbg_x + shadowOffset + self.global_x, boostbg_y + shadowOffset + self.global_y, boostbg_size, boostbg_size , 136 * 16, -91 * 16)
        painter.setPen(QPen(QColor(46, 46, 46), 20, Qt.SolidLine))
        painter.drawArc(boostbg_x + self.global_x, boostbg_y + self.global_y, boostbg_size, boostbg_size, 136 * 16, -91 * 16) 

    def drawGradient(self, painter):
        arc_x = self.global_x - 30
        arc_y = 30 + self.global_y
        arc_width = 550
        arc_height = 550
        start_angle = 332 * 16
        span_angle = 238 * 16

        # Radial Arc
        gradient = QRadialGradient(QPointF(arc_x + arc_width / 2, arc_y + arc_height / 2), arc_width / 2)

        # Add color stops
        gradient.setColorAt(0, QColor(0, 152, 255, 255))  # Fully opaque color
        gradient.setColorAt(1, QColor(0, 0, 0, 20))  # Black, semi-transparent
        # Create a pen with gradient and set it to the painter
        pen = QPen(QBrush(gradient), 140, Qt.SolidLine)
        painter.setPen(pen)

        # Draw the arc
        painter.drawArc(arc_x, arc_y, arc_width, arc_height, start_angle, span_angle)
        painter.drawArc(arc_x, arc_y, arc_width, arc_height, start_angle, span_angle)

    def drawSideArcs(self, painter):    
        pen = QPen(QColor(26, 26, 26))
        pen.setWidth(18)  # Set line width
        painter.setPen(pen)
        painter.setPen(QPen(QColor(26, 26, 26), 25, Qt.SolidLine))
        painter.drawArc(self.global_x - 35, self.global_y, 600, 600, 25 * 16, -50 * 16)   
        painter.setPen(QPen(QColor(26, 26, 26), 25, Qt.SolidLine))
        painter.drawArc(self.global_x - 65, self.global_y, 600, 600, 2480, 50 * 16)
                   
    def drawCenterCircle(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0))
        # Create a pen
        pen = QPen(QColor(0, 0, 0))  # Change this to the color you want for the border
        pen.setWidth(5)  # Change this to set the width of the border
        painter.setPen(pen)

        # Draw the circle
        center_x = 250 + self.global_x # X coordinate of the center of the circle
        center_y = 300 + self.global_y  # Y coordinate of the center of the circle
        radius = 225  # Radius of the circle

        painter.drawEllipse(QPoint(center_x, center_y), radius, radius)                 

class instrumentcluster(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.background = Background(self)
        self.rpm_meter_display = rpm_display(self)
        self.speed_display = speed_display(self)
        self.oil_display = oil_display(self)
        self.afr_display = afr_display(self)
        self.coolant_display = coolant_display(self)
        self.boost_display = boost_display(self)
        self.fuel_display = fuel_display(self)

        self.indicator_lights = IndicatorLights(self)
        self.indicator_lights.setGeometry(0, 0, 1024, 600)
        self.indicator_lights.show()
        
        self.setGeometry(0, 0, 1024, 600)
        self.setStyleSheet("background-color: black;") 

    def show_settings(self):
        self.settings_window.show()  # Make settings window visible.

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw elements from Background
        self.background.drawGradient(painter)
        self.background.drawSideArcs(painter)
        self.background.drawCenterCircle(painter)
        self.background.top_center_bg(painter)

        # Dynamic RPM Redline
        self.rpm_meter_display.drawIndicators(painter)

        # Draw components
        self.rpm_meter_display.widget(painter)
        self.speed_display.widget(painter)
        self.afr_display.widget(painter)
        self.coolant_display.widget(painter)
        self.fuel_display.widget(painter)  
        self.boost_display.widget(painter)
        self.oil_display.widget(painter)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = instrumentcluster()
    mainWin.show()

    sys.exit(app.exec_())
 