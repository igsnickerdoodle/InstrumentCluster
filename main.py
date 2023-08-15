# Needed imports for functioning instrument cluster
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import sys

## Module Imports
from designs.singledial.singledial import Display
#from components.arduino.arduino_serial import ArduinoSerial

## Import Value Update Fields
from components.afr.app_design_1 import AFR
from components.boost.boost_1 import BoostMeter
from components.speed.text import Speed
from components.fuel.fuel_1 import FuelMeter
from components.rpm.rpm_single_display import RpmMeter
from components.oil.oil_temp_1 import OilMeter
from components.coolant_temp.coolant_singledisplay import CoolantGauge
from components.speed.gpsfile import gps

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

        # Create a QLabel, set the pixmap, and set it as the central widget
        label = QLabel()
        self.setCentralWidget(label)
        layout = QGridLayout(label)
        self.display = Display()
        self.display.setAttribute(Qt.WA_TranslucentBackground, True)
        # Grid (row=1, col=0, rowspan=1, colspan=2)       
        layout.addWidget(self.display, 1, 0, 1, 2)  
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('black'))
        self.setPalette(palette)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
