from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QRadialGradient, QBrush
from pathlib import Path
import math, sys

### Local component imports
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))
from designs.singledial import global_x, global_y

from components.rpm.sd_rpm_1 import rpm_display
from components.speed.sd_speed_1 import speed_display
from components.afr.sd_afr_1 import afr_display
from components.boost.sd_boost_1 import boost_display
from components.fuel.sd_fuel_1 import fuel_display
from components.oil.sd_oil_1 import oil_display
from components.coolant_temp.sd_coolant_1 import coolant_display


class Background(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ## Initialize Modules
        self.global_x = global_x
        self.global_y = global_y
        # Setup the swap displays
        # self.current_display = self.boost_display 
        self.create_toggle_buttons()  # Ensure this method is defined
        self.indicator_light_cel = QLabel(self)
        self.indicator_light_highbeams = QLabel(self)
        self.indicator_light_foglights = QLabel(self)

        # Initial / Default 'off' state
        self.cel_on = False
        self.highbeams_on = False
        self.foglights_on = False
        self.max_rpm_value = 8000
        
    def create_toggle_buttons(self):

        # self.toggle_button_center_top = QPushButton("Toggle Center-Top", self)
        # self.toggle_button_center_top.clicked.connect(self.swap_display)
        # self.toggle_button_center_top.setGeometry(10, 170, 120, 40)  # Adjust the size and position as needed
        # self.toggle_button_center_top.setStyleSheet("background-color: red")
        # self.toggle_button_center_top.show()

        self.toggle_button_cel = QPushButton("Toggle CEL", self)
        self.toggle_button_cel.clicked.connect(self.swap_display_cel)
        self.toggle_button_cel.setGeometry(10, 10, 120, 40)
        self.toggle_button_cel.setStyleSheet("background-color: red")
        self.toggle_button_cel.show()

        self.toggle_button_highbeams = QPushButton("Toggle High Beams", self)
        self.toggle_button_highbeams.clicked.connect(self.swap_display_highbeams)
        self.toggle_button_highbeams.setGeometry(10, 60, 120, 40)
        self.toggle_button_highbeams.setStyleSheet("background-color: red")
        self.toggle_button_highbeams.show()

        self.toggle_button_foglights = QPushButton("Toggle Fog Lights", self)
        self.toggle_button_foglights.clicked.connect(self.swap_display_foglights)
        self.toggle_button_foglights.setGeometry(10, 110, 120, 40)
        self.toggle_button_foglights.setStyleSheet("background-color: red")
        self.toggle_button_foglights.show()     

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

    # def swap_display(self):
    #     #print("Button clicked!")  # If this doesn't print, the button is not connected properly
    #     if self.current_display == self.BoostGauge:
    #         self.current_display = self.OilTemp
    #     else:
    #         self.current_display = self.BoostGauge
    #     self.update()

    def drawGradient(self, painter):
        arc_x = self.global_x - 30
        arc_y = 30 + self.global_y
        arc_width = 550
        arc_height = 550
        start_angle = 332 * 16
        span_angle = 238 * 16

        # Create a radial gradient
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

    def drawIndicators(self, painter):
        start_angle = -5  
        end_angle = 269  
        center_angle = (start_angle + end_angle) / 2

        number_offset = 20  
        indicator_length = 8  
        indicator_radius_1 = 290  
        indicator_radius_2 = 293  
        indicator_radius_3 = 294 
        pivot_x = 250 + self.global_x
        pivot_y = 300 + self.global_y
        angle_range = abs(end_angle - start_angle)


        def get_color(rpm_indicator):
            # Determine the color based on RPM range
            if 4500 <= rpm_indicator <= 5500:
                return QColor(129, 196, 255)  # Light sky blue
            elif 5500 <= rpm_indicator <= 6500:
                return QColor(22, 88, 142)  # Yale Blue
            elif 6500 <= rpm_indicator <= 8000:
                return QColor(231, 34, 46)  # Alizarin Crimson
            else:
                return QColor(255, 255, 255)  # Default color (white)
            
        for rpm_indicator in range(0, 9001, 1000):
                if rpm_indicator <= self.max_rpm_value:
                    indicator_length = 8
                    indicator_angle = center_angle + (rpm_indicator / self.max_rpm_value) * angle_range
                    start_x = int(pivot_x + indicator_radius_1 * math.cos(math.radians(indicator_angle)))
                    start_y = int(pivot_y + indicator_radius_1 * math.sin(math.radians(indicator_angle)))
                    end_x = int(start_x + indicator_length * math.cos(math.radians(indicator_angle)))
                    end_y = int(start_y + indicator_length * math.sin(math.radians(indicator_angle)))

                    indicator_pen = QPen(get_color(rpm_indicator), 5, Qt.SolidLine)
                    painter.setPen(indicator_pen)
                    painter.drawLine(start_x, start_y, end_x, end_y)
                    
                    # Add RPM values as numbers
                    rpm_value = rpm_indicator // 1000
                    rpm_value_x = int(pivot_x + (indicator_radius_1 - 0 - number_offset) * math.cos(math.radians(indicator_angle)))
                    rpm_value_y = int(pivot_y + (indicator_radius_1 - 0 - number_offset) * math.sin(math.radians(indicator_angle)))
                    rpm_value_font = QFont("Nimbus Sans", 14)
                    painter.setFont(rpm_value_font)
                    painter.setPen(QColor(255, 255, 255))
                    fontMetrics = painter.fontMetrics()
                    textWidth = fontMetrics.horizontalAdvance(str(rpm_value))
                    textHeight = fontMetrics.height()
                    # Adjust the x and y position considering the text dimensions
                    adjusted_x = int(rpm_value_x - textWidth / 2)
                    adjusted_y = int(rpm_value_y + textHeight / 2)
                    painter.drawText(adjusted_x, adjusted_y, str(rpm_value))

        # Repeat the same logic for the next two loops
        for rpm_indicator in range(0, 9001, 500):
            if rpm_indicator <= self.max_rpm_value and rpm_indicator % 1000 != 0:
                indicator_length = 4
                indicator_angle = center_angle + (rpm_indicator / 8000) * angle_range
                start_x = int(pivot_x + indicator_radius_2 * math.cos(math.radians(indicator_angle)))
                start_y = int(pivot_y + indicator_radius_2 * math.sin(math.radians(indicator_angle)))
                end_x = int(start_x + indicator_length * math.cos(math.radians(indicator_angle)))
                end_y = int(start_y + indicator_length * math.sin(math.radians(indicator_angle)))

                indicator_pen = QPen(get_color(rpm_indicator), 3, Qt.SolidLine)
                painter.setPen(indicator_pen)
                painter.drawLine(start_x, start_y, end_x, end_y)

        for rpm_indicator in range(0, 9001, 100):
            if rpm_indicator <= self.max_rpm_value:
                if rpm_indicator % 500 != 0 and rpm_indicator % 1000 != 0:
                    indicator_length = 2
                    indicator_angle = center_angle + (rpm_indicator / 8000) * angle_range
                    start_x = int(pivot_x + indicator_radius_3 * math.cos(math.radians(indicator_angle)))
                    start_y = int(pivot_y + indicator_radius_3 * math.sin(math.radians(indicator_angle)))
                    end_x = int(start_x + indicator_length * math.cos(math.radians(indicator_angle)))
                    end_y = int(start_y + indicator_length * math.sin(math.radians(indicator_angle)))

                    indicator_pen = QPen(get_color(rpm_indicator), 2, Qt.SolidLine)
                    painter.setPen(indicator_pen)
                    painter.drawLine(start_x, start_y, end_x, end_y)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 255, 255), 3, Qt.SolidLine))
        painter.drawArc(self.global_x - 50, self.global_y, 600, 600, 315 * 16, 271 * 16)

## indicators light section
    def swap_display_cel(self):
        self.indicator_light_cel.setGeometry(238 + self.config.global_x, 500 + self.config.global_y, 30, 30) 
        if self.cel_on:
            self.indicator_light_cel.clear()
            self.cel_on = False
        else:
            pixmap = QPixmap('resources/cel.png')
            pixmap = pixmap.scaled(self.indicator_light_cel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.indicator_light_cel.setPixmap(pixmap)
            self.cel_on = True
        self.indicator_light_cel.show()
    def swap_display_highbeams(self):
        self.indicator_light_highbeams.setGeometry(320 + self.config.global_x, 500 + self.config.global_y, 30, 30)
        if self.highbeams_on:
            self.indicator_light_highbeams.clear()
            self.highbeams_on = False
        else:
            pixmap = QPixmap('resources/High_Beam.png')
            pixmap = pixmap.scaled(self.indicator_light_highbeams.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.indicator_light_highbeams.setPixmap(pixmap)
            self.highbeams_on = True
        self.indicator_light_highbeams.show()
    def swap_display_foglights(self):
        self.indicator_light_foglights.setGeometry(140 + self.config.global_x, 500 + self.config.global_y, 30, 30)
        if self.foglights_on:
            self.indicator_light_foglights.clear()
            self.foglights_on = False
        else:
            pixmap = QPixmap('resources/Fog_light.png')
            pixmap = pixmap.scaled(self.indicator_light_foglights.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.indicator_light_foglights.setPixmap(pixmap)
            self.foglights_on = True
        self.indicator_light_foglights.show()


class Display(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.rpm_meter_display = rpm_display(self)
        self.speed_display = speed_display(self)
        self.background = Background(self)
        self.oil_display = oil_display(self)
        self.afr_display = afr_display(self)
        self.coolant_display = coolant_display(self)
        self.boost_display = boost_display(self)
        self.fuel_display = fuel_display(self)
        
        # Setup the swap displays
        self.current_display = self.boost_display.widget
        
        boost_value = self.boost_display.boost_value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw elements from Background
        self.background.drawGradient(painter)
        self.background.drawSideArcs(painter)
        self.background.drawIndicators(painter)
        self.background.drawCenterCircle(painter)
        self.background.top_center_bg(painter)

        # Draw components
        self.rpm_meter_display.widget(painter)
        self.speed_display.widget(painter)
        self.afr_display.widget(painter)
        self.coolant_display.widget(painter)
        self.fuel_display.widget(painter)  
              
        # self.boost_display.widget(painter)
        # self.oil_display.widget(painter)
        
        # Display swaps
        self.current_display(painter)
    
    def swap_display(self):
        #print("Button clicked!")  # If this doesn't print, the button is not connected properly
        if self.current_display == self.boost_display:
            self.current_display = self.oil_display
        else:
            self.current_display = self.boost_display
        self.update()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = Display()
    mainWin.show()

    sys.exit(app.exec_())

