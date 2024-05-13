from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from __init__ import global_x, global_y
from pathlib import Path
import sys

current_directory = Path(__file__).parent
root_directory = current_directory / '..' / '..'
sys.path.append(str(root_directory.resolve()))
#####################################################
from components.arduino.demo_indicators import ArduinoReader

class IndicatorLights(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ## Initialize Modules
        self.global_x = global_x
        self.global_y = global_y
        
        self.arduino_updater = ArduinoUpdater(self) 

        self.indicator_light_cel = QLabel(self)
        self.indicator_light_highbeams = QLabel(self)
        self.indicator_light_foglights = QLabel(self)
        self.indicator_light_Lturn = QLabel(self)
        self.indicator_light_Rturn = QLabel(self)

        # Initial / Default 'off' state
        self.cel_on = False
        self.highbeams_on = False
        self.foglights_on = False
        self.rturn = False
        self.lturn = False
        self.setStyleSheet("""
        QWidget {
            background-color: transparent;
        }
        QLabel {
            background-color: transparent;
        }
        """)

    def cel(self, turn_on):
        self.indicator_light_cel.setGeometry(238 + self.global_x, 500 + self.global_y, 30, 30)
        if turn_on:
            # pixmap = QPixmap('resources/highbeam.png') # Linux
            pixmap = QPixmap(r'C:\Users\justc\github\InstrumentCluster\resources\cel.png') # Windows
            if pixmap.isNull():
                print("Failed to load resources/cel.png")
            else:
                pixmap = pixmap.scaled(self.indicator_light_cel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.indicator_light_cel.setPixmap(pixmap)
                self.cel_on = True
        else:
            self.indicator_light_cel.clear()
            self.cel_on = False
        self.indicator_light_cel.show()

    def highbeams(self, turn_on):
        self.indicator_light_highbeams.setGeometry(320 + self.global_x, 500 + self.global_y, 30, 30)
        if turn_on:
            # pixmap = QPixmap('resources/highbeam.png') # Linux
            pixmap = QPixmap(r'C:\Users\justc\github\InstrumentCluster\resources\highbeam.png')
            if pixmap.isNull():
                print("Failed to load image from resources/highbeam.png")
            else:
                pixmap = pixmap.scaled(self.indicator_light_highbeams.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.indicator_light_highbeams.setPixmap(pixmap)
                self.highbeams_on = True
        else:
            self.indicator_light_highbeams.clear()
            self.highbeams_on = False
        self.indicator_light_highbeams.show()

    def foglights(self, turn_on):
        self.indicator_light_foglights.setGeometry(140 + self.global_x, 500 + self.global_y, 30, 30)
        if turn_on:
            pixmap = QPixmap(r'C:\Users\justc\github\InstrumentCluster\resources\foglights.png')
            if pixmap.isNull():
                print("Failed to load image from resources/foglights.png")
            else:
                pixmap = pixmap.scaled(self.indicator_light_foglights.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.indicator_light_foglights.setPixmap(pixmap)
                self.foglights_on = True
        else:
            self.indicator_light_foglights.clear()
            self.foglights_on = False
        self.indicator_light_foglights.show()

    def Rturn(self, turn_on):
        self.indicator_light_Rturn.setGeometry(500 + self.global_x, 100 + self.global_y, 20, 30)
        if turn_on:
            pixmap = QPixmap(r'C:\Users\justc\github\InstrumentCluster\resources\rturn.png')
            if pixmap.isNull():
                print("Failed to load image for rturn")
            else:
                pixmap = pixmap.scaled(self.indicator_light_Rturn.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.indicator_light_Rturn.setPixmap(pixmap)
                self.Rturn_on = True
        else:
            self.indicator_light_Rturn.clear()
            self.Rturn_on = False
        self.indicator_light_Rturn.show()

    def Lturn(self, turn_on):
        self.indicator_light_Lturn.setGeometry(-20 + self.global_x, 100 + self.global_y, 20, 30)
        if turn_on:
            pixmap = QPixmap(r'C:\Users\justc\github\InstrumentCluster\resources\lturn.png')
            if pixmap.isNull():
                print("Failed to load image for lturn")
            else:
                pixmap = pixmap.scaled(self.indicator_light_Lturn.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.indicator_light_Lturn.setPixmap(pixmap)
                self.Lturn_on = True
        else:
            self.indicator_light_Lturn.clear()
            self.Lturn_on = False
        self.indicator_light_Lturn.show()

    def updateIndicators(self, painter):
        if self.cel_on:
            self.cel()
        if self.highbeams_on:
            self.highbeams()
        if self.foglights_on:
            self.foglights()
        if self.Rturn_on:
            self.Rturn()
        if self.Lturn_on:
            self.Lturn()

class ArduinoUpdater:
    def __init__(self, indicator_lights):
        self.indicator_lights = indicator_lights
        self.arduino = ArduinoReader()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_from_arduino)
        self.timer.start(100)

    def update_from_arduino(self):
        line = self.arduino.read_line()
        if line:
            print(line)  # For debugging
            if line == "cel_1":
                self.indicator_lights.cel(True)
            elif line == "cel_0":
                self.indicator_lights.cel(False)
            if line == "hb_1":
                self.indicator_lights.highbeams(True)
            elif line == "hb_0":
                self.indicator_lights.highbeams(False)
            if line == "fgl_1":
                self.indicator_lights.foglights(True)
            elif line == "fgl_0":
                self.indicator_lights.foglights(False)
            if line == "rturn_1":
                self.indicator_lights.Rturn(True)
            elif line == "rturn_0":
                self.indicator_lights.Rturn(False)            
            if line == "lturn_1":
                self.indicator_lights.Lturn(True)
            elif line == "lturn_0":
                self.indicator_lights.Lturn(False)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainWin = IndicatorLights()
    mainWin.setGeometry(0, 0, 1024, 600)  # Set the geometry of the main window
    mainWin.show()

    sys.exit(app.exec_())
