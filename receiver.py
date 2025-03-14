import struct
import time
import threading
from receiver_init import ReceiverInit

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
        print(f"DEBUG: Seriele verbinding status: {self.serial}")

    def readData(self):
        print("DEBUG: Thread readData() gestart.")
        if self.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        while self.running:
            # print("DEBUG: readData() is actief")
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

                # time.sleep(0.05)

            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                self.serial.reset_input_buffer()
                time.sleep(1)

    def getLatestData(self):
        return self.latest_data

    def start(self):
        thread = threading.Thread(target=self.readData, daemon=True)
        thread.start()
        print(f"DEBUG: Thread gestart: {thread.is_alive()}")

    def stop(self):
        print("DEBUG: Stopen van ReceiverData!")
        self.running = False
        if self.serial: 
            self.serial.close()
        print("DEBUG: RecveiverDAta gestopt!")

if __name__ == "__main__":
    receiver = ReceiverData()
    receiver.callReceiverInit()
    receiver.start() 

    try:
        while True:
            print("Laatste ontvangen data:", receiver.getLatestData())
            time.sleep(1)  
    except KeyboardInterrupt:
        print("\nStoppen...")
        receiver.stop()
