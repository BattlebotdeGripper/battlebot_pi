import struct
import time
import threading
from receiver.receiver_init import ReceiverInit

class ReceiverData:
    def __init__(self):
        self.serial = None
        self.latest_data = None
        self.running = True 

    def callReceiverInit(self):
        if self.serial is None:
            receiver_init_instance = ReceiverInit()
            self.serial = receiver_init_instance.getSerialConnection()

        if self.serial:
            print("Seriële verbinding met ontvanger succesvol opgezet.")

        else:
            print("Fout bij het opzetten van de seriële verbinding.")

    def readData(self):

        if self.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        while self.running:
            try:
                while self.serial.in_waiting < 32:
                    time.sleep(0.01) 

                serial_data = self.serial.read(32)

                if serial_data[0] == 0x20 and serial_data[1] == 0x40 and len(serial_data) == 32:
                    channels = struct.unpack("<14H", serial_data[2:30])
                    self.latest_data = channels[:3] 
                    
                else:
                    print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    self.serial.reset_input_buffer()

                # time.sleep(0.01)
            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                self.serial.reset_input_buffer()
                # time.sleep(1)

    def getLatestData(self):
        return self.latest_data

    def start(self):
        thread = threading.Thread(target=self.readData, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
        if self.serial: 
            self.serial.close()
