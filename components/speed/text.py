from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics
from . import Config, update_speed_text

class Speed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speed = 0
        self.config = Config()

    def mph(self, painter):
        pivot_x = 250 + self.config.global_x
        pivot_y = 450 + self.config.global_y

        font_size_value = 30  
        font_size_suffix = 10
        
        font_value = QFont('Nimbus Sans', font_size_value)  
        font_suffix = QFont('Nimbus Sans', font_size_suffix)  

        # calculate text dimensions for value
        fontMetrics_value = QFontMetrics(font_value)
        text_width_value = fontMetrics_value.horizontalAdvance("{:.0f}".format(self.speed))
        text_height_value = fontMetrics_value.height()

        # calculate center positions for value
        text_x_value = pivot_x - text_width_value / 2
        text_y_value = pivot_y - text_height_value / 2 + fontMetrics_value.ascent()  # ascent() accounts for baseline offset

        # calculate position for suffix
        text_x_suffix = text_x_value + text_width_value  # Place the "mph" text right after the speed value
        text_y_suffix = text_y_value  # Place the "mph" at the same vertical position as the speed value

        # draw value
        painter.setFont(font_value)
        painter.setPen(QColor(255, 255, 255))  # set text color (here, white)
        painter.drawText(int(text_x_value), int(text_y_value), "{:.0f}".format(self.speed))

        # draw suffix
        painter.setFont(font_suffix)
        painter.drawText(int(text_x_suffix), int(text_y_suffix), " mph")

    update_speed_text = update_speed_text