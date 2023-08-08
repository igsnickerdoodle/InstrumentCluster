from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from . import update_boost
import math

from designs.singledial.singledial import Config

class BoostMeter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.boost_value
        self.fontstyle = "Nimbus Sans Bold"
        self.boost_color = "red, blue, green"
    def display(self, painter, *args, **kwargs):
        boost_value = kwargs.get('boost_value', self.boost_value)
        text_x_offset = -5 
        font_name = self.fontstyle
        bar_color = self.boost_color
        # Parameters for Arc
        pivot_x = 250 + self.config.global_x
        pivot_y = 253 + self.config.global_y

        # Parameter for Max Values
        pivot_text_max_y = 220
        pivot_text_psi_x = 235
        pivot_text_hg_x = 235

        # Parameters for Center Text
        pivot_text_center_y = 220 + self.config.global_y
        pivot_text_center_x = 240 + self.config.global_x
        
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

            color = QColor(bar_color)
            painter.setPen(QPen(color, arc_thickness, Qt.SolidLine))
            painter.drawArc(arc_rect, int(end_angle * 16), int((start_angle - end_angle) * 16))

        # Draw the text labels
        painter.setPen(QColor(255, 255, 255))  
        font = QFont(font_name)
        font.setPointSize(8) 
        painter.setFont(font)
        painter.drawText(int(pivot_text_psi_x + self.config.global_x + rect_size/2), int(pivot_text_max_y), "+30psi")  # Max value label
        painter.drawText(int(pivot_text_hg_x + self.config.global_x - rect_size/2), int(pivot_text_max_y), "-30hg")  # Min value label
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
    def repaint_boost(self):
        rect = QRect(90, 90, 220, 220)  # Define the area to be repainted (Boost gauge region)
        self.repaint(rect)  # Trigger a repaint of the specified region   

    update_boost = update_boost
