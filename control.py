import time
from receiver import ReceiverData
from usb_connection import USBConnection

class Control:
    def __init__(self):
        self.receiver = ReceiverData()
        self.receiver.callReceiverInit()
        self.receiver.start()
        self.USB = USBConnection()

    def run(self):
        while True:
            data = self.receiver.getLatestData()
            if data:
                # print(f"Data: {data}")
                str_data = f"{data}\n"
                print(str_data)
                self.USB.writeData(str_data)
            time.sleep(0.05) # Deze kan veranderd worden om een snellere verbinding te krijgen!

    def start(self):
        self.run() 

if __name__ == "__main__":
    control = Control()

    try:
        control.start() 
    except KeyboardInterrupt:
        print("\nAfsluiten van Control...")
        control.receiver.stop() 