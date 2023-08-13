from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics
from . import update_speed_text, global_x, global_y, font_text_value, font_size_suffix

class Speed(QWidget):
    def __init__(self, parent=None):
        super(Speed, self).__init__(parent)
        self.speed = 0
        self.global_x = global_x
        self.global_y = global_y
        self.font_text_value = font_text_value
        self.font_size_suffix = font_size_suffix
        
    def mph(self, painter):
        pivot_x = 250 + self.global_x
        pivot_y = 450 + self.global_y
        
        font_value = QFont(self.font_text_value)  
        font_suffix = QFont(self.font_size_suffix)  

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