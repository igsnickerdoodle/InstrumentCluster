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
        while self.is_reading:
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
                        self.serial.close()  ## Terminate connection if currently open
                        self.serial.open()
                    except Exception as e:
                        print("Failed to reconnect:", e)
                    return  # Exit the function to avoid getting stuck in a loop
                except Exception as e:
                    print(f"Error while reading values: {e}")

    def start_reading(self):
        self.is_reading = True
        time.sleep(2)  # delay for 2 seconds
        self.serial.write(b'START\n')  # Send "START" command to Arduino data stream
        self.thread = threading.Thread(target=self.read_values)
        self.thread.start()

    def stop_reading(self):
        self.is_reading = False
        self.serial.write(b'STOP\n')  # Send "STOP" command to Arduino end data
        self.serial.close()

arduino = ArduinoSerial('COM3', 57600)
