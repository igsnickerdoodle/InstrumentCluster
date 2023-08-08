## Mandatory import classes
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QRadialGradient, QBrush
import math, sys

from components.coolant_temp.coolant_singledisplay import CoolantGauge
from components.speed.text import Speed
from components.afr.app_design_1 import AFR
from components.boost.boost_1 import BoostMeter
from components.oil.oil_temp_1 import OilMeter
from components.fuel.fuel_1 import FuelMeter
from components.rpm.rpm_single_display import  RpmMeter

class Config:
    def __init__(self):
        ## Sets Global variables for components
        self.global_x = 280
        self.global_y = 50
        self.text_labels = "Nimbus Sans Bold", 8 ## Text in "TextHere", TextSize

class Display(QWidget):
    def __init__(self):
        super().__init__()
        ## Initialize Modules
        self.speed_display = Speed()
        self.afr_display = AFR()
        self.coolant_display = CoolantGauge()
        self.boost_display = BoostMeter()
        self.oil_display = OilMeter()
        self.fuel_display = FuelMeter()
        self.rpm_display = RpmMeter()

        # Setup the swap displays
        self.current_display = self.boost_display 

        self.create_toggle_buttons()  # Ensure this method is defined
        self.indicator_light_cel = QLabel(self)
        self.indicator_light_highbeams = QLabel(self)
        self.indicator_light_foglights = QLabel(self)

        # Initial / Default 'off' state
        self.cel_on = False
        self.highbeams_on = False
        self.foglights_on = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.drawGradient(painter)
        self.drawSideArcs(painter)
        self.drawIndicators(painter)
        self.drawCenterCircle(painter)
        self.top_center_bg(painter)
        self.current_display(painter, self.boost_value)
        self.coolantgauge.CoolantTemp(painter)
        self.afr.AFR()
        self.speed()

    def create_toggle_buttons(self):
        self.toggle_button_center_top = QPushButton("Toggle Center-Top", self)
        self.toggle_button_center_top.clicked.connect(self.swap_display)
        self.toggle_button_center_top.setGeometry(10, 170, 120, 40)  # Adjust the size and position as needed
        self.toggle_button_center_top.setStyleSheet("background-color: red")
        self.toggle_button_center_top.show()

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
        # Boost arc background
        boostbg_x = 35
        boostbg_y = 85
        boostbg_size = 430
        shadowColor = QColor(8, 8, 8, 128)  # Semi-transparent black
        shadowOffset = 2
        painter.setPen(QPen(shadowColor, 20, Qt.SolidLine))
        painter.drawArc(boostbg_x + shadowOffset + self.config.global_x, boostbg_y + shadowOffset + self.config.global_y, boostbg_size, boostbg_size , 136 * 16, -91 * 16)
        painter.setPen(QPen(QColor(46, 46, 46), 20, Qt.SolidLine))
        painter.drawArc(boostbg_x + self.config.global_x, boostbg_y + self.config.global_y, boostbg_size, boostbg_size, 136 * 16, -91 * 16)  
 
    def swap_display(self):
        #print("Button clicked!")  # If this doesn't print, the button is not connected properly
        if self.current_display == self.BoostGauge:
            self.current_display = self.OilTemp
        else:
            self.current_display = self.BoostGauge
        self.update()

    def drawGradient(self, painter):
        arc_x = self.config.global_x - 30
        arc_y = 30 + self.config.global_y
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
        painter.drawArc(self.config.global_x - 35, self.config.global_y, 600, 600, 25 * 16, -50 * 16)   
        painter.setPen(QPen(QColor(26, 26, 26), 25, Qt.SolidLine))
        painter.drawArc(self.config.global_x - 65, self.config.global_y, 600, 600, 2480, 50 * 16)
                   
    def drawCenterCircle(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0))

        # Create a pen
        pen = QPen(QColor(0, 0, 0))  # Change this to the color you want for the border
        pen.setWidth(5)  # Change this to set the width of the border
        painter.setPen(pen)

        # Draw the circle
        center_x = 250 + self.config.global_x # X coordinate of the center of the circle
        center_y = 300 + self.config.global_y  # Y coordinate of the center of the circle
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
        pivot_x = 250 + self.config.global_x
        pivot_y = 300 + self.config.global_y
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
                if rpm_indicator <= 8000:
                    indicator_length = 8
                    indicator_angle = center_angle + (rpm_indicator / 8000) * angle_range
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
            if rpm_indicator <= 8000 and rpm_indicator % 1000 != 0:
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
            if rpm_indicator <= 8000:
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
        painter.drawArc(self.config.global_x - 50, self.config.global_y, 600, 600, 315 * 16, 271 * 16)

    # def BoostGauge(self, painter, *args, **kwargs):
    #     boost_value = kwargs.get('boost_value', self.boost_value)
    #     text_x_offset = -5 
    #     font_name = "Nimbus Sans Bold"

    #     # Parameters for Arc
    #     pivot_x = 250 + self.config.global_x
    #     pivot_y = 253 + self.config.global_y

    #     # Parameter for Max Values
    #     pivot_text_max_y = 220
    #     pivot_text_psi_x = 235
    #     pivot_text_hg_x = 235

    #     # Parameters for Center Text
    #     pivot_text_center_y = 220 + self.config.global_y
    #     pivot_text_center_x = 240 + self.config.global_x
        
    #     rect_size = 255  # Diameter of the gauge
    #     arc_thickness = 15 

    #     # Create the rectangle defining the arc bar area
    #     arc_rect = QRectF(pivot_x - rect_size/2, pivot_y - rect_size/2, rect_size, rect_size)

    #     # If boost_value is positive, draw the positive arc
    #     if boost_value > 0:
    #         start_angle = 90
    #         end_angle = 90 - ((boost_value / 30) * 45) 
    #         # Calculate color based on boost_value
    #         if boost_value <= 15:
    #             color_ratio = boost_value / 15  # Normalize to [0, 1] for green-orange transition
    #             red = int((255 - 0) * color_ratio + 0)  # Transition from green (0, 255, 0) to orange (255, 165, 0)
    #             green = int((165 - 255) * color_ratio + 255)
    #             blue = int((0 - 0) * color_ratio + 0)
    #         else:
    #             color_ratio = (boost_value - 15) / 15  # Normalize to [0, 1] for orange-red transition
    #             red = int((255 - 255) * color_ratio + 255)  # Transition from orange (255, 165, 0) to red (255, 0, 0)
    #             green = int((0 - 165) * color_ratio + 165)
    #             blue = int((0 - 0) * color_ratio + 0)

    #         color = QColor(red, green, blue)
    #         painter.setPen(QPen(color, arc_thickness, Qt.SolidLine))
    #         painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16)) 

    #     # If boost_value is negative, draw the negative arc
    #     elif boost_value < 0:
    #         start_angle = 90
    #         end_angle = 90 + ((abs(boost_value) / 30) * 45)  # Map boost_value onto 90 to 135 degrees

    #         color_ratio = abs(boost_value) / 30  # Normalize to [0, 1] for green-red transition
    #         red = int((255 - 0) * color_ratio)  # Transition from green (0, 255, 0) to red (255, 0, 0)
    #         green = int((0 - 255) * color_ratio + 255)
    #         blue = 0  # Remains 0 as both red and green have 0 blue.

    #         color = QColor(red, green, blue)
    #         painter.setPen(QPen(color, arc_thickness, Qt.SolidLine))
    #         painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16))

    #     # Draw the labels
    #     painter.setPen(QColor(255, 255, 255))  # Set pen color to white for the text
    #     font = QFont(font_name)
    #     font.setPointSize(8)  # Adjust as needed
    #     painter.setFont(font)
    #     painter.drawText(int(pivot_text_psi_x + self.config.global_x + rect_size/2), int(pivot_text_max_y), "+30psi")  # Max value label
    #     painter.drawText(int(pivot_text_hg_x + self.config.global_x - rect_size/2), int(pivot_text_max_y), "-30hg")  # Min value label
    #     if boost_value >= 0:
    #         new_font = QFont(font_name)
    #         new_font.setPointSize(8)
    #         painter.setFont(new_font)
    #         painter.drawText(int(pivot_text_center_x + text_x_offset), 
    #                          int(pivot_y + rect_size/2 - pivot_text_center_y), f'+{boost_value}psi')  # Current value label
    #     else:
    #         new_font = QFont(font_name)
    #         new_font.setPointSize(8)
    #         painter.setFont(new_font)
    #         painter.drawText(int(pivot_text_center_x + text_x_offset), 
    #                          int(pivot_y + rect_size/2 - pivot_text_center_y), f'{boost_value}hg')  # Current value label            
    # def update_boost(self, value):
    #     self.boost_value = int(value)
    #     self.repaint_boost()  # Trigger a repaint of the Boost gauge only        
    # def repaint_boost(self):
    #     rect = QRect(90, 90, 220, 220)  # Define the area to be repainted (Boost gauge region)
    #     self.repaint(rect)  # Trigger a repaint of the specified region   

    # def OilTemp(self, painter, *args, **kwargs):
    #     start_angle = 230
    #     end_angle = 132
    #     major_length = 12
    #     minor_length = 6
    #     needle_radius = 218
    #     major_indicators = {0: major_length, 50: major_length, 100: major_length}
    #     minor_indicators = {25: minor_length, 75: minor_length}
    #     text_labels = {0: "C", 100: "H"}
    #     pivot_x = 250 + self.config.global_x
    #     pivot_y = 295 + self.config.global_y
    #     text_radius = 200
    #     text_angle_offsets = {0: 1, 50: -2.5, 100: -3}
        
    #     # Calculate angle range
    #     angle_range = end_angle - start_angle

    #     # Draw the major indicators
    #     for value, length in major_indicators.items():
    #         value_scaled = (value / 100) * angle_range
    #         indicator_angle = start_angle + value_scaled
    #         indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
    #         indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
    #         indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
    #         indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

    #         # Draw the text labels
    #         if value in text_labels:
    #             text_angle = indicator_angle + text_angle_offsets.get(value, 0)
    #             text_x = pivot_x + text_radius * math.cos(math.radians(90 - text_angle))
    #             text_y = pivot_y + text_radius * math.sin(math.radians(90 - text_angle))
    #             font = QFont("Nimbus Sans", 8)
    #             painter.setFont(font)
    #             painter.setPen(QPen(Qt.white))
    #             painter.drawText(QPointF(text_x, text_y), text_labels[value])

    #         # Draw the indicator
    #         indicator_path = QPainterPath()
    #         indicator_path.moveTo(indicator_start_x, indicator_start_y)
    #         indicator_path.lineTo(indicator_end_x, indicator_end_y)
    #         pen = QPen(Qt.white, 4)  # Adjust the color and thickness as needed
    #         painter.setRenderHint(QPainter.Antialiasing)
    #         painter.setPen(pen)
    #         painter.drawPath(indicator_path)
    #     # Draw the minor indicators
    #     for value, length in minor_indicators.items():
    #         value_scaled = (value / 100) * angle_range
    #         indicator_angle = start_angle + value_scaled
    #         indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
    #         indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
    #         indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
    #         indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

    #         # Draw the indicator
    #         indicator_path = QPainterPath()
    #         indicator_path.moveTo(indicator_start_x, indicator_start_y)
    #         indicator_path.lineTo(indicator_end_x, indicator_end_y)
    #         pen = QPen(Qt.white, 2)  # Adjust the color and thickness as needed
    #         painter.setRenderHint(QPainter.Antialiasing)
    #         painter.setPen(pen)
    #         painter.drawPath(indicator_path)


    #     oil_temp = (self.oil_temp / 260) * 260

    #     # Scale the oil temperature to the range of angles
    #     scaled_oil_temp = ((oil_temp - 0) / (260 - 0)) * (end_angle - start_angle)
    #     # Calculate the needle angle
    #     needle_angle = start_angle + scaled_oil_temp
        
    #     # Compute the start and end points of the needle
    #     start_x = pivot_x + needle_radius * math.cos(math.radians(90 - needle_angle))
    #     start_y = pivot_y + needle_radius * math.sin(math.radians(90 - needle_angle))
    #     end_x = pivot_x + (needle_radius - 10) * math.cos(math.radians(90 - needle_angle))
    #     end_y = pivot_y + (needle_radius - 10) * math.sin(math.radians(90 - needle_angle))

    #     path = QPainterPath()
    #     path.moveTo(start_x, start_y)
    #     path.lineTo(end_x, end_y)
    #     pen = QPen(Qt.red, 4)
    
    #     painter.setPen(pen)
    #     painter.drawPath(path)
        
    #     # Position of the text field
    #     pivot_x_offset = 0  # Adjust this value as desired
    #     text_field_x = pivot_x + pivot_x_offset
    #     text_field_y = pivot_y + self.config.global_y - 240

    #     # Draw the text field with the current value
    #     oiltemp_font = QFont("Nimbus Sans Bold", 10) 
    #     painter.setFont(oiltemp_font)
    #     painter.setPen(QPen(Qt.white))  # Adjust color as needed

    #     ## Display OilTemp in Text 
    #     text = str(round(((self.oil_temp / 260) * 260))) + 'C'
    #     # Calculate the text width
    #     metrics = QFontMetrics(font)
    #     width = metrics.width(text)
    #     text_field_x_adjusted = text_field_x - width / 2  
    #     # Draw the text
    #     painter.drawText(QPointF(text_field_x_adjusted, text_field_y), text)
    # def update_oil_temp(self, value):
    #     # Update the Fuel value based on the slider position
    #     self.oil_temp = int(value)
    #     self.repaint_oil_temp()  # Trigger a repaint of the widget without clearing the background
    # def repaint_oil_temp(self):
    #     self.update()

    # def RpmNeedle(self, painter):
    #     pivot_x = 250 + self.config.global_x
    #     pivot_y = 300 + self.config.global_y

    #     start_angle = -5
    #     end_angle = 269
    #     center_angle = (start_angle + end_angle) / 2
    #     needle_radius = 260
    #     angle_range = abs(end_angle - start_angle)
    #     needle_angle = center_angle + (self.rpm / 8000) * angle_range
    #     ## RPM needle image import
    #     pixmap = QPixmap('resources/rpmneedle.png')
    #     ## Secondary resize on the rpm needle 
    #     pixmap = pixmap.scaled(QSize(26, 90),Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    #     # Calculate needle position
    #     needle_x = pivot_x + needle_radius * math.cos(math.radians(needle_angle)) - pixmap.width() / 2
    #     needle_y = pivot_y + needle_radius * math.sin(math.radians(needle_angle)) - pixmap.height() / 2
    #     transform = QTransform()
    #     transform.translate(needle_x + pixmap.width() / 2, needle_y + pixmap.height() / 2)
    #     transform.rotate(-270)  # Initial rotation to align with angle = 0 upward.
    #     transform.rotate(needle_angle)
    #     transform.translate(-needle_x - pixmap.width() / 2, -needle_y - pixmap.height() / 2)
    #     # Draw pixmap centered on pivot point
    #     painter.setTransform(transform)
    #     painter.drawPixmap(int(needle_x), int(needle_y), pixmap)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     # Reset transformation after drawing
    #     painter.resetTransform()
    # def update_rpm(self, value):
    #     self.rpm = int(value)
    #     self.repaint_rpm()
    # def repaint_rpm(self):
        self.update()

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
       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
                
        # Create a ArcWidget instance
        self.tachometer = Display()

        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 1024, 600)

        # Create a QWidget and set it as the central widget
        central_widget = Display()
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
