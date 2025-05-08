import serial

class ReceiverInit:
    def __init__(self) -> None:
        self.url: str = "/dev/serial0"
        self.baudrate: int = 115200
        self.timeout: int = 0.1
        self.serial: serial.Serial | None = None

    def setUpSerialConnection(self) -> None:
        try:
            self.serial = serial.Serial(self.url, self.baudrate, timeout=self.timeout)
            print(f"Verbonden met {self.url} op {self.baudrate} baud")
            self.serial.reset_input_buffer() 

        except serial.SerialException as e:
            print(f"Kan seriële verbinding niet openen: {e}")
            self.serial = None

    def getSerialConnection(self) -> serial.Serial | None:
        if self.serial == None:
            self.setUpSerialConnection()
        return self.serial