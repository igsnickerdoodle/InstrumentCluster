from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QTransform, QPixmap, QColor, QFont, QPen
from PyQt5.QtWidgets import QWidget, QApplication
import math, sys
from pathlib import Path

# Ensure that the correct modules and methods are imported.
current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))

from components.rpm import global_x, global_y, update_rpm

class rpm_display(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.global_x = global_x
        self.global_y = global_y
        self.rpm = 0
        self.max_rpm_value = 8000  # Renamed for consistency
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color:transparent;")

    def widget(self, painter):
        pivot_x = 250 + self.global_x
        pivot_y = 300 + self.global_y
        start_angle = -5
        end_angle = 269
        center_angle = (start_angle + end_angle) / 2
        needle_radius = 260
        angle_range = abs(end_angle - start_angle)

        # Calculate the needle angle based on current rpm
        needle_angle = center_angle + (self.rpm / self.max_rpm_value) * angle_range
        pixmap = QPixmap('resources/rpmneedle.png')
        pixmap = pixmap.scaled(QSize(26, 90), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        
        needle_x = pivot_x + needle_radius * math.cos(math.radians(needle_angle)) - pixmap.width() / 2
        needle_y = pivot_y + needle_radius * math.sin(math.radians(needle_angle)) - pixmap.height() / 2
        transform = QTransform()
        transform.translate(needle_x + pixmap.width() / 2, needle_y + pixmap.height() / 2)
        transform.rotate(-270 + needle_angle)  # Adjusted rotation
        transform.translate(-needle_x - pixmap.width() / 2, -needle_y - pixmap.height() / 2)

        painter.setTransform(transform)
        painter.drawPixmap(int(needle_x), int(needle_y), pixmap)
        painter.resetTransform()  # Reset transformation after drawing

    def repaint_rpm(self):
        self.update()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = rpm_display()
    mainWin.show()

    sys.exit(app.exec_())