from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette, QColor
from arduino_serial import arduino
from left_dial import Tachometer
from right_dial import Speedometer
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.left_dial = Tachometer()
        self.right_dial = Speedometer()
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # updates every 1 second

    def init_ui(self):
        # initialize your UI here, add left and right dial to layout
        layout = QHBoxLayout()
        layout.addWidget(self.left_dial)
        layout.addWidget(self.right_dial)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.resize(1024, 600)
    def update(self):
        # This method will be called every 1 second, you can read data from Arduino and pass it to the dials here
        current_values = arduino.current_values
        if current_values:
            left_data = current_values.get('left')  # Adjust these to match the actual keys in your JSON data
            right_data = current_values.get('right')  # Adjust these to match the actual keys in your JSON data
            if left_data is not None:
                self.left_dial.update_data(left_data)
            if right_data is not None:
                self.right_dial.update_data(right_data)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Set background color to black
    palette = QPalette()
    palette.setColor(QPalette.Background, QColor('black'))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    arduino.start_reading()  # Start reading from Arduino here
    sys.exit(app.exec_())
    arduino.stop_reading()  # This might not be called if the app doesn't exit normally
