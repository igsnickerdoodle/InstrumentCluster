    def FuelNeedle(self, painter):
        start_angle = 298
        end_angle = 242
        major_length = 12
        minor_length = 6
        needle_radius = 300
        major_indicators = {0: major_length, 50: major_length, 100: major_length}
        minor_indicators = {25: minor_length, 75: minor_length}
        text_labels = {0: "E", 100: "F"}
        pivot_x = 235 + self.config.global_x
        pivot_y = 300 + self.config.global_y
        text_radius = 300
        text_angle_offsets = {0: 3, 50: -2.5, 100: -3}        
    
        # Display "Low Fuel" warning when fuel level is >= 13%
        if self.fuel <= 13:
            image_path = 'resources/low_fuel_indicator.png'  # Replace with the actual image file path
            warning_icon = QPixmap(image_path)

            # Scale the image
            scaled_size = QSize(23, 23)
            warning_icon = warning_icon.scaled(scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Fine tune image x,y positions
            image_x_position = self.config.global_x - 45
            image_y_position = 460 + self.config.global_y 

            # Draw the image
            painter.drawPixmap(QPoint(image_x_position, image_y_position), warning_icon)
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
