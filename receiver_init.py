import serial

class ReceiverInit:
    def __init__(self, url="/dev/serial0", baudrate=115200, timeout=1):
        self.url = url  
        self.baudrate = baudrate  
        self.timeout = timeout

        try:
            self.serial = serial.Serial(self.url, self.baudrate, timeout=self.timeout)
            print(f"Verbonden met {self.url} op {self.baudrate} baud")
            self.serial.reset_input_buffer() 

        except serial.SerialException as e:
            print(f"Kan seriële verbinding niet openen: {e}")
            self.serial = None

    def getSerialConnection(self):
        return self.serial