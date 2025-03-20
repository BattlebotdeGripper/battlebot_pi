import serial
import time

class USBConnection:

    def __init__(self, url="/dev/ttyACM0", baudrate=115200, timeout=1):
        self.url = url  
        self.baudrate = baudrate  
        self.timeout = timeout
        self.serial_usb = serial.Serial(self.url, baudrate=self.baudrate, timeout=self.timeout)

    # def setUpUSBSerialConnection()

    def sendSerial(self, serial):
        self.serial_usb.write((serial + "\n").encode())
        self.serial_usb.flush()
        # time.sleep(1)

        print(serial)

# import serial
# import time

# ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)

# def sendSerial(serial):
#     ser.write((serial + "\n").encode())
#     ser.flush()
#     time.sleep(0.5)

#     print(serial)