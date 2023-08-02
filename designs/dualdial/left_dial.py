from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QGridLayout, QSpacerItem, QSizePolicy, QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSize, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath, QFont, QPixmap, QTransform, QFontMetrics
import math, sys

class Tachometer(QWidget):
    def __init__(self):
        super().__init__()     
   
        ## Initialize default values
        self.boost_value = 0
        self.rpm = 0
        self.coolant = 0
        self.afr_value = 14.7
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawArcs(painter)
        self.drawIndicators(painter)
        self.RpmNeedle(painter)
        self.drawCenterCircle(painter)
        self.BoostGauge(painter, self.boost_value)
        self.CoolantTemp(painter)
        self.AFR(painter)
    
    def drawArcs(self, painter):
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
                         
    def drawIndicators(self, painter):
        start_angle = -5  
        end_angle = 269  
        center_angle = (start_angle + end_angle) / 2

        number_offset = 20  
        indicator_length = 8  
        indicator_radius_1 = 200  # Modify as needed
        indicator_radius_2 = 202  # Modify as needed
        indicator_radius_3 = 203  # Modify as needed
        pivot_x = 250
        pivot_y = 250
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
        painter.drawArc(40, 40, 420, 420, 315 * 16, 271 * 16)

    def BoostGauge(self, painter, boost_value, font_name="Nimbus Sans Bold",text_x_offset=-5):
        # Parameters for Arc
        pivot_x = 250
        pivot_y = 253
        # Parameter for Max Values
        pivot_text_max_y = 200
        pivot_text_psi_x = 195
        pivot_text_hg_x = 280
        # Parameters for Center Text
        pivot_text_center_y = 235
        pivot_text_center_x = 240
        
        rect_size = 255  # Diameter of the gauge, adjust as needed
        arc_thickness = 15  # Thickness of the arc bar

        # Create the rectangle defining the arc bar area
        arc_rect = QRectF(pivot_x - rect_size/2, pivot_y - rect_size/2, rect_size, rect_size)

        # If boost_value is positive, draw the positive arc
        if boost_value > 0:
            start_angle = 90
            end_angle = 90 - ((boost_value / 30) * 45)  # Map boost_value onto 90 to 45 degrees

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
            painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16))  # Multiply by 16 because Qt measures angles in 1/16th degrees

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
            painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16))  # Multiply by 16 because Qt measures angles in 1/16th degrees

        # Draw the labels
        painter.setPen(QColor(255, 255, 255))  # Set pen color to white for the text
        font = QFont(font_name)
        font.setPointSize(8)  # Adjust as needed
        painter.setFont(font)
        painter.drawText(int(pivot_text_psi_x + rect_size/2), int(pivot_text_max_y), "+30psi")  # Max value label
        painter.drawText(int(pivot_text_hg_x - rect_size/2), int(pivot_text_max_y), "-30hg")  # Min value label
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

    def RpmNeedle(self, painter):
        pivot_x = 250
        pivot_y = 250

        start_angle = -5
        end_angle = 269
        center_angle = (start_angle + end_angle) / 2
        needle_radius = 165
        angle_range = abs(end_angle - start_angle)
        needle_angle = center_angle + (self.rpm / 8000) * angle_range

        pixmap = QPixmap('C:/Users/justc/Documents/git/InstrumentCluster/dual-display/resources/rpmneedle.png')
        

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
        # Define your bar here
        origin_x = 125
        origin_y = 420
        bar_length = 250
        bar_width = 10
        major_length = 12
        minor_length = 6
        needle_length = 10  # Add control over needle length

        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "C", 100: "H"}
        textx = -5
        texty = 40

        # Draw the bar
        painter.setPen(QPen(QColor(46, 46, 46), bar_width, Qt.SolidLine))
        painter.drawLine(int(origin_x), int(origin_y), int(origin_x + bar_length), int(origin_y))

        # Draw the major indicators
        for value, length in major_indicators.items():
            value_scaled = (value / 100) * bar_length
            indicator_start_x = origin_x + value_scaled
            indicator_start_y = origin_y - length / 2
            indicator_end_y = origin_y + length / 2

            # Draw the text labels
            if value in text_labels:
                text_x = indicator_start_x
                text_y = origin_y - length / 2 - 10
                font = QFont("DejaVu Sans", 8)
                painter.setFont(font)
                painter.setPen(QPen(Qt.white))
                painter.drawText(QPointF(int(text_x + textx), int(text_y + texty)), text_labels[value])

            # Draw the indicator
            pen = QPen(Qt.white, 4)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawLine(int(indicator_start_x), int(indicator_start_y), int(indicator_start_x), int(indicator_end_y))

        # Draw the minor indicators
        for value, length in minor_indicators.items():
            value_scaled = (value / 100) * bar_length
            indicator_start_x = origin_x + value_scaled
            indicator_start_y = origin_y - length / 2
            indicator_end_y = origin_y + length / 2

            # Draw the indicator
            pen = QPen(Qt.white, 2)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(pen)
            painter.drawLine(int(indicator_start_x), int(indicator_start_y), int(indicator_start_x), int(indicator_end_y))

        # Scale the coolant level to the bar length
        coolant_scaled = (self.coolant / 100) * bar_length

        # Draw the needle
        needle_x = origin_x + coolant_scaled
        needle_start_y = origin_y - needle_length / 2  # Adjust the start and end of needle according to the new length
        needle_end_y = origin_y + needle_length / 2

        pen = QPen(Qt.red, 4)
        painter.setPen(pen)
        painter.drawLine(int(needle_x), int(needle_start_y), int(needle_x), int(needle_end_y))

    def update_coolant(self, value):
        # Update the Fuel value based on the slider position
        self.coolant = int(value)
        self.repaint_coolant()  # Trigger a repaint of the widget without clearing the background

    def repaint_coolant(self):
        self.update()

    def AFR(self, painter):
        # Set the position where the text will be centered
        center_x = 250
        center_y = 360

        # Set the font details
        font = QFont("Nimbus Sans Bold", 12)
        painter.setFont(font)

        # Create the text string with the AFR value
        text_string = "{:.2f}".format(self.afr_value)

        # Calculate the width of the text
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(text_string)

        # Calculate the starting position of the text
        text_x = center_x - text_width / 2

        # Draw the shadow first, offset by +2 in the x and y direction, color it black
        painter.setPen(QPen(Qt.black))
        painter.drawText(QPointF(text_x + 2, center_y + 2), text_string)

        # Then draw the main white text
        painter.setPen(QPen(Qt.white))
        painter.drawText(QPointF(text_x, center_y), text_string)


        start_angle = -45
        end_angle = 45
        major_length = 10
        minor_length = 3
        needle_radius = 135
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "Rich", 100: "Lean"}
        pivot_x = 250
        pivot_y = 247
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
        text_field_x = pivot_x  + -5 # Adjust these values as desired
        text_field_y = pivot_y + -75  # Adjust these values as desired

        # Draw the text field with the current value
        font = QFont("Nimbus Sans", 10)  # Adjust font size as needed
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))  # Adjust color as needed
        painter.drawText(QPointF(text_field_x, text_field_y), str(self.afr_value))  # Use the afr_value directly

    def update_afr(self, value):
        # Update the Fuel value based on the slider position
        self.afr_value = float(value) / 100
        self.repaint_afr()  # Trigger a repaint of the widget without clearing the background

    def repaint_afr(self):
        self.update()

    def update_data(self, data):
        if "RPM" in data:
            self.update_speed(data["RPM"])
        if "Boost" in data:
            self.update_oil_temp(data["Boost"])
        if "AFR" in data:
            self.update_fuel(data["AFR"])
        if "Coolant Tempt" in data:
            self.update_fuel(data["Coolant Temp"])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the background to black
        self.setStyleSheet("background-color: black;")


        # Create a ArcWidget instance
        self.arcWidget = Tachometer()

        # Set the geometry of the MainWindow
        self.setGeometry(0, 0, 1920, 480)

        # Create a QWidget and set it as the central widget
        central_widget = Tachometer()
        self.setCentralWidget(central_widget)

        # Create a QHBoxLayout, add the arc widget to it and add a stretch
        layout = QHBoxLayout()
        layout.addWidget(self.arcWidget)
        layout.addStretch(1)
        
        # Set the layout of the central widget
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)



    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())