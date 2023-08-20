# Needed imports for functioning instrument cluster
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import sys

## Module Imports
from designs.singledial.singledial import Display
from designs.dualdial.application import DualDisplay
#from components.arduino.arduino_serial import ArduinoSerial

## Import Value Update Fields
from components.afr.sd_afr_1 import afr_display
from components.boost.sd_boost_1 import boost_display
from components.speed.sd_speed_1 import speed_display
from components.fuel.sd_fuel_1 import fuel_display
from components.rpm.sd_rpm_1 import rpm_display
from components.oil.sd_oil_1 import oil_display
from components.coolant_temp.sd_coolant_1 import coolant_display
from components.speed.gpsfile import gps
from components.speed.sd_speed_1  import speed_display

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1024, 600)
        # self.update_values = ValueUpdate()

        label = QLabel()
        self.setCentralWidget(label)
        layout = QGridLayout(label)
        self.display = Display()
        self.display.setAttribute(Qt.WA_TranslucentBackground, True)              
        layout.addWidget(self.display, 1, 0, 1, 2)  
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('black'))
        self.setPalette(palette)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
