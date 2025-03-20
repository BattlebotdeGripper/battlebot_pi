import time
import serial
from receiver.receiver import ReceiverData
from usb.connection import USBConnection
# from usb.connection import sendSerial

class Control:

    # pin=16 - Linkerwiel - channel=1
    # pin=17 - Rechterwiel - channel=2

    def __init__(self):
        self.receiver = ReceiverData()
        self.receiver.callReceiverInit()
        self.receiver.start()
        self.usb_connection = USBConnection()
        self.ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
        self.ser.setDTR(False)
        self.ser.setRTS(False)  

    def run(self):

        while True:
            data = self.receiver.getLatestData()
            if data:
                str_data = f"{data}\n"

                try:
                    self.usb_connection.sendSerial(str_data)
                    # sendSerial(str_data)
                    # self.ser.write((str_data + "\n").encode())
                    # self.ser.flush()
                    print(str_data)
                    pass
                except ValueError:
                    print("Geen geldige data ontvangen!")

            time.sleep(0.1) # Deze kan veranderd worden om een snellere verbinding te krijgen!

if __name__ == "__main__":
    control = Control()

    try:
        control.run() 

    except KeyboardInterrupt:
        print("\nAfsluiten van Control...")