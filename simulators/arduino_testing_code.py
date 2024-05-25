class ArduinoUpdater:
    def __init__(self, indicator_lights, main_window):
        # Input Signals
        self.indicator_lights = indicator_lights
        self.main_window = main_window

        ## Init Arduino
        self.arduino = ArduinoReader()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_from_arduino)
        ## Adjust Timer settings for needs
        self.timer.start(100)

    def update_from_arduino(self):
        line = self.arduino.read_line()
        if line:
            print(line)  # For debugging
            if line.strip() == "0x344":
                self.main_window.show_settings()

## Disabled for Development Purposing

# class ValueUpdate:
#     def __init__(self):
#         super().__init__()
#         ## Initialize Serial Connections
#         self.gps = gps()
#         self.arduino = ArduinoSerial()   
#         ## Initial component updates
#         self.speed_value = Speed.update_speed  
#         self.afr_value = AFR.update_afr
#         self.coolant_value = CoolantGauge.update_coolant
#         self.boost_value = BoostMeter.update_boost
#         self.oil_value = OilMeter.update_oil_temp
#         self.fuel_value = FuelMeter.update_fuel
#         self.rpm_value = RpmMeter.update_rpm

#         ## Initialize Update Refresh Rate
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_arduino_values, self.update_gps_value)
#         self.timer.start(50)  # Update every 1000 milliseconds (1 second)

#     def update_arduino_values(self):
#         self.arduino.read_values()
#         arduino_current_values = self.arduino.current_values

#         if "RPM" in arduino_current_values:
#             self.rpm_value(arduino_current_values["RPM"])
#         if "Coolant Temp" in arduino_current_values:
#             self.coolant_value(arduino_current_values["Coolant Temp"])
#         if "Boost" in arduino_current_values:
#             self.boost_value(arduino_current_values["Boost"])  
#         if "AFR" in arduino_current_values:
#             self.afr_value(arduino_current_values["AFR"])
#         if "Oil Temp" in arduino_current_values:
#             self.oil_value(arduino_current_values["Oil Temp"])
#         if "Fuel" in arduino_current_values:
#             self.fuel_value(arduino_current_values["Fuel"])
    
#     def update_gps_value(self):
#         self.gps.read_values()
#         gps_current_values = self.gps.get_speed

#         if "MPH" in gps_current_values:
#             self.rpm_value(gps_current_values["MPH"])