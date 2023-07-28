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
                # Try to parse the line as JSON
                json_line = json.loads(line)
                # If the line is valid JSON, update the current values
                self.current_values = json_line
                print(self.current_values)  # Print the current values
            except json.JSONDecodeError:
                # If the line is not valid JSON, ignore it
                pass
            except serial.serialutil.SerialException:
                print("Serial connection lost. Attempting to reconnect...")
                try:
                    self.serial.close()  # Close the serial connection before trying to reopen it
                    self.serial.open()
                except Exception as e:
                    print("Failed to reconnect:", e)
                return  # Exit the function to avoid getting stuck in a loop
            except Exception as e:
                print(f"Error while reading values: {e}")

    def start_reading(self):
        self.is_reading = True
        time.sleep(2)  # delay for 2 seconds
        self.serial.write(b'START\n')  # Send "START" command to Arduino
        while self.is_reading:
            self.read_values()

    def stop_reading(self):
        self.is_reading = False
        self.serial.write(b'STOP\n')  # Send "STOP" command to Arduino
        self.serial.close()

arduino = ArduinoSerial('/dev/ttyACM0', 115200)  # Replace with your port and baud rate

# Register the stop_reading function to be called on exit
atexit.register(arduino.stop_reading)

# Start reading values
thread = threading.Thread(target=arduino.start_reading)
thread.start()

# Stop reading values
# arduino.stop_reading()
