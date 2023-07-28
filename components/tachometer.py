from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSize, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath, QFont, QPixmap, QTransform, QFontMetrics, QRadialGradient, QBrush
import math, sys

#from components.arduino_serial import arduino
from arduino_serial import arduino
#from speedometer import Speedometer

global_x = 280
global_y = 50

class Tachometer(QWidget):
    def __init__(self):
        super().__init__()

        self.arduino = arduino       

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(50)  # Update every 1000 milliseconds (1 second)

        ## Initialize Start Values
        self.boost_value = 0
        self.rpm = 0
        self.coolant = 0
        self.afr_value = 14.7
        self.speed = 0
        self.oil_temp = 0
        self.fuel = 0
        
        # Setup the initial display
        self.current_display = self.BoostGauge
        self.create_toggle_buttons()
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
        self.drawArcs(painter)
        self.drawIndicators(painter)
        self.RpmNeedle(painter)              
        self.drawCenterCircle(painter)
        self.current_display(painter, self.boost_value)
        self.CoolantTemp(painter)
        self.AFR(painter)
        self.mph(painter)
        self.FuelNeedle(painter)
        
    def update_values(self):
        self.arduino.read_values()
        current_values = self.arduino.current_values

        if "RPM" in current_values:
            self.update_rpm(current_values["RPM"])
        if "Coolant Temp" in current_values:
            self.update_coolant(current_values["Coolant Temp"])
        if "Boost" in current_values:
            self.update_boost(current_values["Boost"])  
        if "AFR" in current_values:
            self.update_afr(current_values["AFR"])
        if "Oil Temp" in current_values:
            self.update_oil_temp(current_values["Oil Temp"])
        if "Fuel" in current_values:
            self.update_fuel(current_values["Fuel"])

#        self.speedometer.get_speed()
#        current_MPH = self.MPH.current_MPH
        
#       if "MPH" in current_MPH:
#            self.update_speed(current_values["MPH"])

    def create_toggle_buttons(self):

        toggle_button_center_top = QPushButton("Toggle Center-Top", self)
        toggle_button_center_top.clicked.connect(self.swap_display)
        toggle_button_center_top.setGeometry(10, 10, 120, 40)  # Adjust the size and position as needed
        toggle_button_center_top.setStyleSheet("background-color: red")
        toggle_button_center_top.show()

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
        
    def swap_display(self):
        if self.current_display == self.BoostGauge:
            self.current_display = self.OilTemp
    
        else:
            self.current_display = self.BoostGauge

    def drawArcs(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
  
 
        # Define arc parameters
        arc_x = 60 + global_x
        arc_y = 55 + global_y
        arc_width = 375
        arc_height = 375
        start_angle = 332 * 16
        span_angle = 238 * 16

        # Create a radial gradient
        gradient = QRadialGradient(QPointF(arc_x + arc_width / 2, arc_y + arc_height / 2), arc_width / 2)

        # Add color stops
        gradient.setColorAt(0, QColor(0, 152, 255, 255))  # Bright red, fully opaque
        gradient.setColorAt(1, QColor(0, 0, 0, 20))  # Black, semi-transparent


        # Create a pen with gradient and set it to the painter
        pen = QPen(QBrush(gradient), 140, Qt.SolidLine)
        painter.setPen(pen)

        # Draw the arc
        painter.drawArc(arc_x, arc_y, arc_width, arc_height, start_angle, span_angle)

        # Set the color and width of the circle's outline
        pen = QPen(QColor(26, 26, 26))  # Set color (here, red)
        pen.setWidth(18)  # Set line width
        painter.setPen(pen)
        

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(26, 26, 26), 25, Qt.SolidLine))
        painter.drawArc(70 + global_x, 40 + global_y, 420, 420, 25 * 16, -50 * 16)   
        
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(26, 26, 26), 25, Qt.SolidLine))
        painter.drawArc(10 + global_x, 40 + global_y, 420, 420, 2480, 50 * 16)
                   
    def drawCenterCircle(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        # Set the fill color of the circle
        painter.setBrush(QColor(26, 26, 26))  # Fill color (here, green)
        # Draw the circle
        center_x = 250 + global_x # X coordinate of the center of the circle
        center_y = 250 + global_y  # Y coordinate of the center of the circle
        radius = 135  # Radius of the circle
        painter.drawEllipse(QPoint(center_x, center_y), radius, radius)   
        
        # Boost arc background
        shadowColor = QColor(0, 0, 0, 128)  # Semi-transparent black
        shadowOffset = 2
        painter.setPen(QPen(shadowColor, 20, Qt.SolidLine))
        painter.drawArc(125 + shadowOffset + global_x, 125 + shadowOffset + global_y, 250, 250 , 136 * 16, -91 * 16)
        painter.setPen(QPen(QColor(46, 46, 46), 20, Qt.SolidLine))
        painter.drawArc(125+ global_x, 125 + global_y, 250, 250, 136 * 16, -91 * 16)                       
    def drawIndicators(self, painter):
        start_angle = -5  
        end_angle = 269  
        center_angle = (start_angle + end_angle) / 2

        number_offset = 20  
        indicator_length = 8  
        indicator_radius_1 = 200  
        indicator_radius_2 = 202  
        indicator_radius_3 = 203 
        pivot_x = 250 + global_x
        pivot_y = 250 + global_y
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
        # Creates the Tachometer and Outline
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 255, 255), 3, Qt.SolidLine))
        painter.drawArc(40 + global_x, 40 + global_y, 420, 420, 315 * 16, 271 * 16)

    def BoostGauge(self, painter, *args, **kwargs):
        boost_value = kwargs.get('boost_value', self.boost_value)
        text_x_offset = -5 
        font_name = "Nimbus Sans Bold"
        # Parameters for Arc
        pivot_x = 250 + global_x
        pivot_y = 253 + global_y
        # Parameter for Max Values
        pivot_text_max_y = 200
        pivot_text_psi_x = 195
        pivot_text_hg_x = 280
        # Parameters for Center Text
        pivot_text_center_y = 235 + global_y
        pivot_text_center_x = 240 + global_x
        
        rect_size = 255  # Diameter of the gauge
        arc_thickness = 15 

        # Create the rectangle defining the arc bar area
        arc_rect = QRectF(pivot_x - rect_size/2, pivot_y - rect_size/2, rect_size, rect_size)

        # If boost_value is positive, draw the positive arc
        if boost_value > 0:
            start_angle = 90
            end_angle = 90 - ((boost_value / 30) * 45) 
            # Calculate color based on boost_value
            if boost_value <= 15:
                color_ratio = boost_value / 15  # Normalize to [0, 1] for green-orange transition
                red = int((255 - 0) * color_ratio + 0)  # Transition from green (0, 255, 0) to orange (255, 165, 0)
                green = int((165 - 255) * color_ratio + 255)
                blue = int((0 - 0) * color_ratio + 0)
            else:
                color_ratio = (boost_value - 15) / 15  # Normalize to [0, 1] for orange-red transition
                red = int((255 - 255) * color_ratio + 255)  # Transition from orange (255, 165, 0) to red (255, 0, 0)
                green = int((0 - 165) * color_ratio + 165)
                blue = int((0 - 0) * color_ratio + 0)

            color = QColor(red, green, blue)
            painter.setPen(QPen(color, arc_thickness, Qt.SolidLine))
            painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16)) 

        # If boost_value is negative, draw the negative arc
        elif boost_value < 0:
            start_angle = 90
            end_angle = 90 + ((abs(boost_value) / 30) * 45)  # Map boost_value onto 90 to 135 degrees

            color_ratio = abs(boost_value) / 30  # Normalize to [0, 1] for green-red transition
            red = int((255 - 0) * color_ratio)  # Transition from green (0, 255, 0) to red (255, 0, 0)
            green = int((0 - 255) * color_ratio + 255)
            blue = 0  # Remains 0 as both red and green have 0 blue.

            color = QColor(red, green, blue)
            painter.setPen(QPen(color, arc_thickness, Qt.SolidLine))
            painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16))

        # Draw the labels
        painter.setPen(QColor(255, 255, 255))  # Set pen color to white for the text
        font = QFont(font_name)
        font.setPointSize(8)  # Adjust as needed
        painter.setFont(font)
        painter.drawText(int(pivot_text_psi_x + global_x + rect_size/2), int(pivot_text_max_y), "+30psi")  # Max value label
        painter.drawText(int(pivot_text_hg_x + global_x - rect_size/2), int(pivot_text_max_y), "-30hg")  # Min value label
        if boost_value >= 0:
            new_font = QFont(font_name)
            new_font.setPointSize(8)
            painter.setFont(new_font)
            painter.drawText(int(pivot_text_center_x + text_x_offset), 
                             int(pivot_y + rect_size/2 - pivot_text_center_y), f'+{boost_value}psi')  # Current value label
        else:
            new_font = QFont(font_name)
            new_font.setPointSize(8)
            painter.setFont(new_font)
            painter.drawText(int(pivot_text_center_x + text_x_offset), 
                             int(pivot_y + rect_size/2 - pivot_text_center_y), f'{boost_value}hg')  # Current value label
    def update_boost(self, value):
        self.boost_value = int(value)
        self.repaint_boost()  # Trigger a repaint of the Boost gauge only        
    def repaint_boost(self):
        rect = QRect(90, 90, 220, 220)  # Define the area to be repainted (Boost gauge region)
        self.repaint(rect)  # Trigger a repaint of the specified region   

    def OilTemp(self, painter, *args, **kwargs):
        start_angle = 230
        end_angle = 130
        major_length = 12
        minor_length = 6
        needle_radius = 135
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "C", 100: "H"}
        pivot_x = 250 + global_x
        pivot_y = 253 + global_y
        text_radius = 100
        text_angle_offsets = {0: 1, 50: -2.5, 100: -3}
        # Calculate angle range
        angle_range = end_angle - start_angle

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the text labels
            if value in text_labels:
                text_angle = indicator_angle + text_angle_offsets.get(value, 0)
                text_x = pivot_x + text_radius * math.cos(math.radians(90 - text_angle))
                text_y = pivot_y + text_radius * math.sin(math.radians(90 - text_angle))
                font = QFont("Nimbus Sans", 8)
                painter.setFont(font)
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPointF(text_x, text_y), text_labels[value])

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 4)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        # Draw the minor indicators
        for value, length in minor_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 2)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)


        oil_temp = (self.oil_temp / 260) * 260

        # Scale the oil temperature to the range of angles
        scaled_oil_temp = ((oil_temp - 0) / (260 - 0)) * (end_angle - start_angle)
        # Calculate the needle angle
        needle_angle = start_angle + scaled_oil_temp
        
        # Compute the start and end points of the needle
        start_x = pivot_x + needle_radius * math.cos(math.radians(90 - needle_angle))
        start_y = pivot_y + needle_radius * math.sin(math.radians(90 - needle_angle))
        end_x = pivot_x + (needle_radius - 10) * math.cos(math.radians(90 - needle_angle))
        end_y = pivot_y + (needle_radius - 10) * math.sin(math.radians(90 - needle_angle))
        path = QPainterPath()
        path.moveTo(start_x, start_y)
        path.lineTo(end_x, end_y)
        pen = QPen(Qt.red, 4)
    
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Position of the text field
        pivot_x_offset = 0  # Adjust this value as desired
        text_field_x = pivot_x + pivot_x_offset
        text_field_y = pivot_y + -100  + global_y 

        # Draw the text field with the current value
        font = QFont("Nimbus Sans Bold", 11) 
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))  # Adjust color as needed

        # Your text
        text = str(round(((self.oil_temp / 260) * 260))) + 'C'

        # Calculate the text width
        metrics = QFontMetrics(font)
        width = metrics.width(text)

        # Adjust the x-coordinate
        text_field_x_adjusted = text_field_x - width / 2  

        # Draw the text
        painter.drawText(QPointF(text_field_x_adjusted, text_field_y), text)
    def update_oil_temp(self, value):
        # Update the Fuel value based on the slider position
        self.oil_temp = int(value)
        self.repaint_oil_temp()  # Trigger a repaint of the widget without clearing the background
    def repaint_oil_temp(self):
        self.update()

    def RpmNeedle(self, painter):
        pivot_x = 250 + global_x
        pivot_y = 250 + global_y

        start_angle = -5
        end_angle = 269
        center_angle = (start_angle + end_angle) / 2
        needle_radius = 165
        angle_range = abs(end_angle - start_angle)
        needle_angle = center_angle + (self.rpm / 8000) * angle_range

        pixmap = QPixmap('/srv/pyapp/resources/rpmneedle.png')
        

        # Resize the pixmap
        pixmap = pixmap.scaled(QSize(26, 90),Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # Calculate needle position
        needle_x = pivot_x + needle_radius * math.cos(math.radians(needle_angle)) - pixmap.width() / 2
        needle_y = pivot_y + needle_radius * math.sin(math.radians(needle_angle)) - pixmap.height() / 2

        transform = QTransform()
        transform.translate(needle_x + pixmap.width() / 2, needle_y + pixmap.height() / 2)
        transform.rotate(-270)  # Initial rotation to align with angle = 0 upward.
        transform.rotate(needle_angle)
        transform.translate(-needle_x - pixmap.width() / 2, -needle_y - pixmap.height() / 2)

        # Draw pixmap centered on pivot point
        painter.setTransform(transform)
        painter.drawPixmap(int(needle_x), int(needle_y), pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Reset transformation after drawing
        painter.resetTransform()
    def update_rpm(self, value):
        self.rpm = int(value)
        self.repaint_rpm()
    def repaint_rpm(self):
        self.update()

    def CoolantTemp(self, painter):
        start_angle = 60
        end_angle = 120
        major_length = 12
        minor_length = 6
        needle_radius = 210
        major_indicators = {0: major_length, 210: major_length, 420: major_length}
        minor_indicators = {105: minor_length, 315: minor_length}
        text_labels = {0: "C", 420: "H"}
        pivot_x = 290 + global_x
        pivot_y = 250 + global_y
        
        text_radius = 185
        text_angle_offsets = {0: 3, 210: -2.5, 420: -3}
        
        # Calculate angle range
        angle_range = end_angle - start_angle

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = ((value - 0) / (420 - 0)) * angle_range  # Rescale to the new range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the text labels
            if value in text_labels:
                text_angle = indicator_angle + text_angle_offsets.get(value, 0)
                text_x = pivot_x + text_radius * math.cos(math.radians(90 - text_angle))
                text_y = pivot_y + text_radius * math.sin(math.radians(90 - text_angle))
                font = QFont("Nimbus Sans", 8)
                painter.setFont(font)
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPointF(text_x, text_y), text_labels[value])

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 4)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        # Draw the minor indicators
        for value, length in minor_indicators.items():
            value_scaled = ((value - 0) / (420 - 0)) * angle_range  # Rescale to the new range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 2)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        # If temperature is below 210 or above 215, scale normally
        if self.coolant < 210 or self.coolant > 215:
            temp_scaled = ((self.coolant - 0) / (420 - 0)) * angle_range  # Rescale to the new range
        # If temperature is within buffer zone (210 - 215), hold the needle at 210 position
        elif 210 <= self.coolant <= 215:
            temp_scaled = ((210 - 0) / (420 - 0)) * angle_range  # Use the lower limit of the buffer zone to scale
        if self.coolant >= 220:
            # Load the image from resources folder
 #           image_path = '/srv/pyapp/resources/coolant_warning_icon.png'  # Replace with the actual image file path
 #           warning_icon = QPixmap(image_path)
 #           if warning_icon.isNull():
 #              print(f"Warning: Unable to load image at {image_path}")

            # Scale the image
            scaled_size = QSize(25, 25)  # Replace with your desired size
            warning_icon = warning_icon.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Set the position where you want to draw the image
            image_x_position = 442 + global_x  # Replace with the actual x-coordinate
            image_y_position = 118 + global_y # Replace with the actual y-coordinate

            # Draw the image
            painter.drawPixmap(QPoint(image_x_position, image_y_position), warning_icon)


        # Calculate the needle angle
        needle_angle = start_angle + temp_scaled

        # Compute the start and end points of the needle
        start_x = pivot_x + needle_radius * math.cos(math.radians(90 - needle_angle))
        start_y = pivot_y + needle_radius * math.sin(math.radians(90 - needle_angle))
        end_x = pivot_x + (needle_radius - 10) * math.cos(math.radians(90 - needle_angle))
        end_y = pivot_y + (needle_radius - 10) * math.sin(math.radians(90 - needle_angle))

        path = QPainterPath()
        path.moveTo(start_x, start_y)
        path.lineTo(end_x, end_y)
        pen = QPen(Qt.red, 4)
        painter.setPen(pen)
        painter.drawPath(path)
    def update_coolant(self, value):
        # Update the Fuel value based on the slider position
        self.coolant = int(value)
        self.repaint_coolant()  # Trigger a repaint of the widget without clearing the background
    def repaint_coolant(self):
        self.update()

    def AFR(self, painter):
        start_angle = -45
        end_angle = 45
        major_length = 10
        minor_length = 3
        needle_radius = 135
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "Rich", 100: "Lean"}
        pivot_x = 250 + global_x
        pivot_y = 247 + global_y
        text_radius = 115
        text_angle_offsets = {0: 0, 0: 0, 0: 0}
        # Calculate angle range
        angle_range = end_angle - start_angle

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))
            # Draw the text labels
            if value in text_labels:
                text_angle = indicator_angle + text_angle_offsets.get(value, 0)
                text_x = pivot_x + text_radius * math.cos(math.radians(90 - text_angle))
                text_y = pivot_y + text_radius * math.sin(math.radians(90 - text_angle))
                font = QFont("Nimbus Sans", 8)
                painter.setFont(font)
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPointF(text_x, text_y), text_labels[value])
            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 4)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)
        # Draw the minor indicators
        for value, length in minor_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 2)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        afr_value_scaled = ((self.afr_value - 8.5) / (18 - 8.5)) * angle_range
        # Calculate the needle angle
        needle_angle = start_angle + afr_value_scaled

        # Compute the start and end points of the needle
        start_x = pivot_x + needle_radius * math.cos(math.radians(90 - needle_angle))
        start_y = pivot_y + needle_radius * math.sin(math.radians(90 - needle_angle))
        end_x = pivot_x + (needle_radius - 10) * math.cos(math.radians(90 - needle_angle))
        end_y = pivot_y + (needle_radius - 10) * math.sin(math.radians(90 - needle_angle))
        path = QPainterPath()
        path.moveTo(start_x, start_y)
        path.lineTo(end_x, end_y)
        pen = QPen(Qt.red, 4)

        painter.setPen(pen)
        painter.drawPath(path)

        # Position of the text field
        text_field_x = pivot_x  + -10 # Adjust these values as desired
        text_field_y = pivot_y + 115  # Adjust these values as desired

        # Draw the text field with the current value
        font = QFont("Nimbus Sans", 10)  # Adjust font size as needed
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))  # Adjust color as needed
        painter.drawText(QPointF(text_field_x, text_field_y), str(self.afr_value))  # Use the afr_value directly
    def update_afr(self, value):
        self.afr_value = float(value) / 100
        self.repaint_afr()
    def repaint_afr(self):
        self.update()


    def mph(self, painter):
        pivot_x = 250 + global_x
        pivot_y = 250 + global_y

        font_size_value = 30  
        font_size_suffix = 10
        
        font_value = QFont('Nimbus Sans', font_size_value)  
        font_suffix = QFont('Nimbus Sans', font_size_suffix)  

        # calculate text dimensions for value
        fontMetrics_value = QFontMetrics(font_value)
        text_width_value = fontMetrics_value.horizontalAdvance("{:.0f}".format(self.speed))
        text_height_value = fontMetrics_value.height()

        # calculate text dimensions for suffix
        fontMetrics_suffix = QFontMetrics(font_suffix)
        text_width_suffix = fontMetrics_suffix.horizontalAdvance(" mph")
        text_height_suffix = fontMetrics_suffix.height()

        # calculate center positions for value
        text_x_value = pivot_x - text_width_value / 2
        text_y_value = pivot_y - text_height_value / 2 + fontMetrics_value.ascent()  # ascent() accounts for baseline offset

        # calculate position for suffix
        text_x_suffix = pivot_x - text_width_suffix / 2  # Center the "mph" text
        text_y_suffix = pivot_y + text_height_value / 2 + text_height_suffix  # adjust this to align the suffix under the line

        # draw value
        painter.setFont(font_value)
        painter.setPen(QColor(255, 255, 255))  # set text color (here, white)
        painter.drawText(int(text_x_value), int(text_y_value), "{:.0f}".format(self.speed))

        # Draw a longer line
        line_y = pivot_y + text_height_value / 2  # place the line under the text
        painter.drawLine(int(text_x_value - 10), int(line_y), int(text_x_value + text_width_value + 10), int(line_y))

        # draw suffix
        painter.setFont(font_suffix)
        painter.drawText(int(text_x_suffix), int(text_y_suffix), "mph")
    def update_speed(self, value):
        self.speed = int(value)

    def FuelNeedle(self, painter):
        start_angle = 300  
        end_angle = 240
        major_length = 12
        minor_length = 6
        needle_radius = 210
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "E", 50: "1/2", 100: "F"}
        pivot_x = 210 + global_x
        pivot_y = 250 + global_y
        
#        low_fuel_x = 150 + global_x
#       low_fuel_y = 190 + global_y
        # Calculate "Low Fuel" warning position
#        warning_x = low_fuel_x
#        warning_y = low_fuel_y + low_fuel_text_radius
                
        text_radius = 190
#        low_fuel_text_radius = 145
        text_angle_offsets = {0: 3, 50: -2.5, 100: -3}
    
        # Display "Low Fuel" warning when fuel level is >= 13%
#        if self.fuel <= 13:
#            image_path = '/srv/pyapp/resources/low_fuel_indicator.png'  # Replace with the actual image file path
#            warning_icon = QPixmap(image_path)
            # Debugging
#            if warning_icon.isNull():
#                print(f"Warning: Unable to load image at {image_path}")

            # Scale the image
#            scaled_size = QSize(23, 23)
#            warning_icon = warning_icon.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Fine tune image x,y positions
#            image_x_position = 35 + global_x 
#            image_y_position = 358 + global_y 

            # Draw the image
#            painter.drawPixmap(QPoint(image_x_position, image_y_position), warning_icon)


        # Calculate angle range
        angle_range = end_angle - start_angle

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the text labels
            if value in text_labels:
                text_angle = indicator_angle + text_angle_offsets.get(value, 0)
                text_x = pivot_x + text_radius * math.cos(math.radians(90 - text_angle))
                text_y = pivot_y + text_radius * math.sin(math.radians(90 - text_angle))
                font = QFont("Nimbus Sans", 8)
                painter.setFont(font)
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPointF(text_x, text_y), text_labels[value])

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 4)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        # Draw the minor indicators
        for value, length in minor_indicators.items():
            value_scaled = (value / 100) * angle_range
            indicator_angle = start_angle + value_scaled
            indicator_start_x = pivot_x + (needle_radius - length) * math.cos(math.radians(90 - indicator_angle))
            indicator_start_y = pivot_y + (needle_radius - length) * math.sin(math.radians(90 - indicator_angle))
            indicator_end_x = pivot_x + needle_radius * math.cos(math.radians(90 - indicator_angle))
            indicator_end_y = pivot_y + needle_radius * math.sin(math.radians(90 - indicator_angle))

            # Draw the indicator
            indicator_path = QPainterPath()
            indicator_path.moveTo(indicator_start_x, indicator_start_y)
            indicator_path.lineTo(indicator_end_x, indicator_end_y)
            pen = QPen(Qt.white, 2)  # Adjust the color and thickness as needed
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawPath(indicator_path)

        # Scale the fuel level to the range of angles
        fuel_scaled = (self.fuel / 100) * angle_range
        # Calculate the needle angle
        needle_angle = start_angle + fuel_scaled
        # Calculates the start and end points of the needle
        start_x = pivot_x + needle_radius * math.cos(math.radians(90 - needle_angle))
        start_y = pivot_y + needle_radius * math.sin(math.radians(90 - needle_angle))
        end_x = pivot_x + (needle_radius - 10) * math.cos(math.radians(90 - needle_angle))
        end_y = pivot_y + (needle_radius - 10) * math.sin(math.radians(90 - needle_angle))

        path = QPainterPath()
        path.moveTo(start_x, start_y)
        path.lineTo(end_x, end_y)
        pen = QPen(Qt.red, 4)
        painter.setPen(pen)
        painter.drawPath(path)
    def update_fuel(self, value):
        self.fuel = int(value)
        self.repaint_fuel()
    def repaint_fuel(self):
        self.update()

    def swap_display_cel(self):
        self.indicator_light_cel.setGeometry(238 + global_x, 390 + global_y, 30, 30) 
        if self.cel_on:
            self.indicator_light_cel.clear()
            self.cel_on = False
        else:
            pixmap = QPixmap('/srv/pyapp/resources/cel.png')
            pixmap = pixmap.scaled(self.indicator_light_cel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.indicator_light_cel.setPixmap(pixmap)
            self.cel_on = True
        self.indicator_light_cel.show()

    def swap_display_highbeams(self):
        self.indicator_light_highbeams.setGeometry(320 + global_x, 390 + global_y, 30, 30)
        if self.highbeams_on:
            self.indicator_light_highbeams.clear()
            self.highbeams_on = False
        else:
            pixmap = QPixmap('/srv/pyapp/resources/High_Beam.png')
            pixmap = pixmap.scaled(self.indicator_light_highbeams.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.indicator_light_highbeams.setPixmap(pixmap)
            self.highbeams_on = True
        self.indicator_light_highbeams.show()

    def swap_display_foglights(self):
        self.indicator_light_foglights.setGeometry(140 + global_x, 390 + global_y, 30, 30)
        if self.foglights_on:
            self.indicator_light_foglights.clear()
            self.foglights_on = False
        else:
            pixmap = QPixmap('/srv/pyapp/resources/Fog_light.png')
            pixmap = pixmap.scaled(self.indicator_light_foglights.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.indicator_light_foglights.setPixmap(pixmap)
            self.foglights_on = True
        self.indicator_light_foglights.show()
       
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")        
        # Create a ArcWidget instance
        self.tachometer = Tachometer()
        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 1024, 600)
        # Create a QWidget and set it as the central widget
        central_widget = Tachometer()
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
