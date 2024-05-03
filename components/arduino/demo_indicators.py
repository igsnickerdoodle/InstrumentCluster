# arduino_reader.py
import serial
import time

class ArduinoReader:
    def __init__(self, port='COM3', baudrate=9600):
        self.ser = serial.Serial(port, baudrate)
        self.ser.flush()

    def read_line(self):
        if self.ser.in_waiting > 0:
            return self.ser.readline().decode('utf-8').strip()
        return None

    def close(self):
        self.ser.close()