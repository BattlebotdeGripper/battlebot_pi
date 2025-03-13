import serial

class USBConnection:

    def __init__(self, url="/dev/ttyACM0", baudrate=115200, timeout=1):
        self.url = url
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = serial.Serial(self.url, self.baudrate, self.timeout)

    def getUSBConnection(self, data):

        try:
            while True:
                self.serial.write(data.encode())
                response = self.serial.readline().decode().strip()
                print(f"Pico antwoord: {response}")

        except KeyboardInterrupt:
            print("Verbinding handmatig verbroken!")