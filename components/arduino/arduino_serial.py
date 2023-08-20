import atexit
import serial
import json
import threading
import time

class ArduinoSerial:
    def __init__(self, port, baud_rate):
        self.serial = serial.Serial(port, baud_rate)
        self.current_values = {}
        self.is_reading = False

    def read_values(self):
        while self.serial.in_waiting:
            try:
                line = self.serial.readline().decode(errors='replace').strip()
                json_line = json.loads(line)
                self.current_values = json_line
                print(self.current_values) 
            except json.JSONDecodeError:
                pass
            except serial.serialutil.SerialException:
                print("Serial connection lost. Attempting to reconnect...")
                try:
                    self.serial.close()
                    self.serial.open()
                except Exception as e:
                    print("Failed to reconnect:", e)
                return
            except Exception as e:
                print(f"Error while reading values: {e}")

    def start_reading(self):
        self.is_reading = True
        time.sleep(2) 
        self.serial.write(b'START\n') 
        while self.is_reading:
            self.read_values()

    def stop_reading(self):
        self.is_reading = False
        self.serial.write(b'STOP\n')
        self.serial.close()

# Replace with your port and baud rate
# For Windows check Device Manager. It will be a COM port
# For Linux please check /dev/ and dmesg

arduino = ArduinoSerial('COM3', 57600)  

# Register the stop_reading function to be called on exit
atexit.register(arduino.stop_reading)

# Start reading values
thread = threading.Thread(target=arduino.start_reading)
thread.start()

# Stop reading values
# arduino.stop_reading()
