import serial, time

class ArduinoReader:
    _instance = None

    def __new__(cls, port='COM4', baudrate=9600):
        if cls._instance is None:
            cls._instance = super(ArduinoReader, cls).__new__(cls)
            # Put any initialization here.
            cls._instance.ser = serial.Serial(port, baudrate)
            cls._instance.ser.flush()
        return cls._instance

    def read_line(self):
        if self.ser.in_waiting > 0:
            return self.ser.readline().decode('utf-8').strip()
        return None

    def close(self):
        self.ser.close()