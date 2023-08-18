import serial
import pynmea2
import time

class gps:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.set_baud_rate(115200)
        time.sleep(1)  # Wait for the baudrate to be applied
        self.ser.baudrate = 115200  # Change baudrate on Python side
        self.set_update_rate(100)

    def get_speed(self):
        line = self.ser.readline().decode('ascii', errors='replace')
        if line.startswith(('$GPRMC', '$GNRMC')):
            try:
                return self.parse_gps(line)
            except pynmea2.ParseError as e:
                print(f'Parse error: {e}')
        return None

    def parse_gps(self, data):
        msg = pynmea2.parse(data)
        if isinstance(msg, pynmea2.types.talker.RMC):
            speed_mph = msg.spd_over_grnd * 1.15078
            return f"MPH {round(speed_mph)}"
    def set_baud_rate(self, rate):
        command = f'$PMTK251,{rate}'
        checksum = 0
        for char in command[1:]:
            checksum ^= ord(char)
        checksum = format(checksum, '02X')
        command += '*' + checksum + '\r\n'
        self.ser.write(command.encode('ascii'))
    def set_update_rate(self, rate):
        command = f'$PMTK220,{rate}'
        checksum = 0
        for char in command[1:]:
            checksum ^= ord(char)
        checksum = format(checksum, '02X')
        command += '*' + checksum + '\r\n'
        self.ser.write(command.encode('ascii'))