from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QGroupBox
from PyQt5.QtCore import Qt, QPointF, QSize, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath, QFont, QPixmap, QTransform, QFontMetrics
import math, sys
#from components.arduino_serial import arduino
from arduino_serial import arduino



class Speedometer(QWidget):
    def __init__(self):
        super().__init__()
        self.arduino = arduino
        
        # Create a QTimer to update the RPM value periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(50)  # Update every 1000 milliseconds (1 second)


        # Define additional properties if needed, e.g.:
        self.fuel = 0
        self.speed = 0
        self.oil_temp = 0
        
      
      
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawDials(painter)
        self.drawIndicators(painter)
        self.Speed(painter)
        self.drawCenterCircle(painter)
        self.mph(painter)         
        self.FuelNeedle(painter)
        self.OilTemp(painter)         
  
    def drawIndicators(self, painter):
        start_angle = -5  
        end_angle = 269  
        center_angle = (start_angle + end_angle) / 2

        number_offset = 20  
        major_indicator_length = 8  
        minor_indicator_length = 3  # Modify as needed
        major_indicator_width = 2  # Modify as needed
        minor_indicator_width = 1  # Modify as needed
        indicator_radius_1 = 200  # Modify as needed
        indicator_radius_2 = indicator_radius_1 + 5  # Adjusted based on minor indicator length
        pivot_x = 250
        pivot_y = 250
        angle_range = abs(end_angle - start_angle)

        for speed_indicator in range(0, 181, 2):
            if speed_indicator % 10 == 0:  # Major indicator
                indicator_length = major_indicator_length
                indicator_width = major_indicator_width
                indicator_radius = indicator_radius_1
            else:  # Minor indicator
                indicator_length = minor_indicator_length
                indicator_width = minor_indicator_width
                indicator_radius = indicator_radius_2

            indicator_angle = center_angle + (speed_indicator / 180) * angle_range
            start_x = int(pivot_x + indicator_radius * math.cos(math.radians(indicator_angle)))
            start_y = int(pivot_y + indicator_radius * math.sin(math.radians(indicator_angle)))
            end_x = int(start_x + indicator_length * math.cos(math.radians(indicator_angle)))
            end_y = int(start_y + indicator_length * math.sin(math.radians(indicator_angle)))

            indicator_pen = QPen(QColor(255, 255, 255), indicator_width, Qt.SolidLine)
            painter.setPen(indicator_pen)
            painter.drawLine(start_x, start_y, end_x, end_y)

            # Add speed values as numbers for major indicators
            if speed_indicator % 10 == 0:
                speed_value = speed_indicator
                speed_value_x = int(pivot_x + (indicator_radius - 0 - number_offset) * math.cos(math.radians(indicator_angle)))
                speed_value_y = int(pivot_y + (indicator_radius - 0 - number_offset) * math.sin(math.radians(indicator_angle)))
                speed_value_font = QFont("Nimbus Sans", 12)
                painter.setFont(speed_value_font)
                painter.setPen(QColor(255, 255, 255))
                fontMetrics = painter.fontMetrics()
                textWidth = fontMetrics.horizontalAdvance(str(speed_value))
                textHeight = fontMetrics.height()
                # Adjust the x and y position considering the text dimensions
                adjusted_x = int(speed_value_x - textWidth / 2)
                adjusted_y = int(speed_value_y + textHeight / 2)
                painter.drawText(adjusted_x, adjusted_y, str(speed_value))

        # Creates the Tachometer and Outline
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 255, 255), 2, Qt.SolidLine))
        painter.drawArc(40, 40, 420, 420, 315 * 16, 271 * 16)
    def drawDials(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        # Creates the Tachometer and Outline
        painter.setPen(QPen(QColor(26, 26, 26), 25, Qt.SolidLine))
        painter.drawArc(50, 50, 400, 400, 318 * 16, 266 * 16)
         
        # Set the color and width of the circle's outline
        pen = QPen(QColor(26, 26, 26))  # Set color (here, red)
        pen.setWidth(18)  # Set line width
        painter.setPen(pen)
    def drawCenterCircle(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        # Set the fill color of the circle
        painter.setBrush(QColor(26, 26, 26))  # Fill color (here, green)
        # Draw the circle
        center_x = 250 # X coordinate of the center of the circle
        center_y = 250  # Y coordinate of the center of the circle
        radius = 135  # Radius of the circle
        painter.drawEllipse(QPoint(center_x, center_y), radius, radius)   
        
        # Boost arc background
        shadowColor = QColor(0, 0, 0, 128)  # Semi-transparent black
        shadowOffset = 2
        painter.setPen(QPen(shadowColor, 20, Qt.SolidLine))
        painter.drawArc(125 + shadowOffset, 125 + shadowOffset, 250, 250, 136 * 16, -91 * 16)
        painter.setPen(QPen(QColor(46, 46, 46), 20, Qt.SolidLine))
        painter.drawArc(125, 125, 250, 250, 136 * 16, -91 * 16)   
       
 
    def Speed(self, painter):
        pivot_x = 250
        pivot_y = 250

        start_angle = -5
        end_angle = 269
        center_angle = (start_angle + end_angle) / 2
        needle_radius = 165
        angle_range = abs(end_angle - start_angle)
        needle_angle = center_angle + (self.speed / 180) * angle_range

        pixmap = QPixmap('C:/Users/justc/Documents/git/InstrumentCluster/dual-display/resources/speedneedle.png')

        # Resize the pixmap
        pixmap = pixmap.scaled(QSize(26, 90), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Calculate needle position
        needle_x = pivot_x + needle_radius * math.cos(math.radians(needle_angle)) - pixmap.width()/2
        needle_y = pivot_y + needle_radius * math.sin(math.radians(needle_angle)) - pixmap.height()/2

        transform = QTransform()
        transform.translate(needle_x + pixmap.width()/2, needle_y + pixmap.height()/2)
        transform.rotate(-270)  # Initial rotation to align with angle = 0 upward.
        transform.rotate(needle_angle)
        transform.translate(-needle_x - pixmap.width()/2, -needle_y - pixmap.height()/2)

        # Draw pixmap centered on pivot point
        painter.setTransform(transform)
        painter.drawPixmap(int(needle_x), int(needle_y), pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Reset transformation after drawing
        painter.resetTransform()
    def mph(self, painter):
        pivot_x = 250
        pivot_y = 250
        font_size = 20  # replace with your desired font size
        font = QFont('Nimbus Sans', font_size)  # replace 'Arial' with your desired font

        # Calculate text dimensions
        fontMetrics = QFontMetrics(font)
        text_width = fontMetrics.horizontalAdvance("{:.0f}".format(self.speed))
        text_height = fontMetrics.height()

        # Calculate center positions
        text_x = pivot_x - text_width / 2
        text_y = pivot_y - text_height / 2 + fontMetrics.ascent()  # ascent() accounts for baseline offset

        text_x = int(text_x)
        text_y = int(text_y)

        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # set text color (here, white)
        painter.drawText(text_x, text_y, "{:.0f}".format(self.speed))

        # Draw a longer line
        line_y = text_y + int(text_height / 4)  # place the line under the text
        painter.drawLine(text_x - 10, line_y, text_x + text_width + 10, line_y)
    def update_speed(self, value):
        # Update the speed value based on the slider position
        self.speed = int(value)
        self.repaint_speed()  # Trigger a repaint of the widget without clearing the background
    def repaint_speed(self):
        self.update()



    def FuelNeedle(self, painter):
        start_angle = -39  
        end_angle = 41
        major_length = 12
        minor_length = 6
        needle_radius = 170
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "E", 50: "1/2", 100: "F"}
        pivot_x = 250
        pivot_y = 280
        
        low_fuel_x =150
        low_fuel_y = 190
        
        text_radius = 145
        low_fuel_text_radius = 145
        text_angle_offsets = {0: 3, 50: -2.5, 100: -3}
        
        # Calculate "Low Fuel" warning position
        warning_x = low_fuel_x
        warning_y = low_fuel_y + low_fuel_text_radius

        # Display "Low Fuel" warning when fuel level is >= 13
        if self.fuel <= 13:
            font = QFont("Nimbus Sans", 10)
            painter.setFont(font)
            painter.setPen(QPen(Qt.red))
            painter.drawText(QPointF(warning_x, warning_y), "Low Fuel")


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
    def update_fuel(self, value):
        # Update the Fuel value based on the slider position
        self.fuel = int(value)
        self.repaint_fuel()  # Trigger a repaint of the widget without clearing the background
    def repaint_fuel(self):
        self.update()



    def OilTemp(self, painter):
        start_angle = 230
        end_angle = 130
        major_length = 12
        minor_length = 6
        needle_radius = 135
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "C", 100: "H"}
        pivot_x = 250
        pivot_y = 270
        text_radius = 80
        text_angle_offsets = {0: 3, 50: -2.5, 100: -3}
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
        text_field_x = pivot_x  + -5 # Adjust these values as desired
        text_field_y = pivot_y + -75  # Adjust these values as desired

        # Draw the text field with the current value
        font = QFont("Nimbus Sans", 10)  # Adjust font size as needed
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))  # Adjust color as needed
        painter.drawText(QPointF(text_field_x, text_field_y), str(round((self.oil_temp / 260) * 260)))        
    def update_oil_temp(self, value):
        # Update the Fuel value based on the slider position
        self.oil_temp = int(value)
        self.repaint_oil_temp()  # Trigger a repaint of the widget without clearing the background
    def repaint_oil_temp(self):
        self.update()



    def update_values(self):
        self.arduino.read_values()
        current_values = self.arduino.current_values

        if "MPH" in current_values:
            self.update_speed(current_values["MPH"])
        if "Oil Temp" in current_values:
            self.update_oil_temp(current_values["Oil Temp"])  
        if "Fuel" in current_values:
            self.update_fuel(current_values["Fuel"])  
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the background to black
        self.setStyleSheet("background-color: black;")

        # Create a central widget
        self.central_widget = QWidget()

        # Create a Speedometer instance
        self.arcWidget = Speedometer()

        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 800, 480)

        # Create a QHBoxLayout
        layout = QHBoxLayout()

        # Add a stretch factor to the layout to push the widget to the right

        # Add the widget to the layout
        layout.addWidget(self.arcWidget)

        # Set the layout of the central widget
        self.central_widget.setLayout(layout)

        # Set the central widget of the MainWindow
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())