import serial
import time

class USBConnection:
    def __init__(self, url="/dev/ttyACM0", baudrate=115200, timeout=1):
        self.serial = serial.Serial(url, baudrate=baudrate, timeout=timeout)

    def writeData(self, data):
        if isinstance(data, str):
            data = data.encode()  # Zet string om naar bytes
        self.serial.write(data)
        time.sleep(0.01)  # 10ms delay voor stabiliteit
    