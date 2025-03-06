import struct
from control import Control
from receiver_init import ReceiverInit
import time

class ReceiverData:
    def __init__(self):    
        serial_init = ReceiverInit()
        self.serial = serial_init.getSerialConnection()                             
        # led = Led()
        self.control = Control()

    def readData(self):
        if self.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        while True:
            try:
                while self.serial.in_waiting < 32:
                    time.sleep(0.01) 

                data = self.serial.read(32)

                if data[0] == 0x20 and data[1] == 0x40 and len(data) == 32:

                    channels = struct.unpack("<14H", data[2:30])
                    self.control.run(channels)

                else:
                    print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    self.serial.reset_input_buffer()

                time.sleep(0.001)

            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                self.serial.reset_input_buffer()
                time.sleep(1) 

    def writeData(self):
        pass

if __name__ == "__main__":
    try:
        get_ibus_data = ReceiverData()
        channels = get_ibus_data.readData()
    except Exception as e:
        print(f"Error: {e}")
