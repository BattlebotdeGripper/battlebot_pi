import time
from receiver import ReceiverData

class Control:
    def __init__(self):
        self.receiver = ReceiverData()
        self.receiver.callReceiverInit()
        self.receiver.start()

    def run(self):
        while True:
            data = self.receiver.getLatestData()
            if data:
                print(f"Ontvangen data in Control: {data}")
                # print(type(data))
            time.sleep(0.025) # Deze kan veranderd worden om een snellere verbinding te krijgen!

    def start(self):
        self.run() 

if __name__ == "__main__":
    control = Control()

    try:
        control.start() 
    except KeyboardInterrupt:
        print("\nAfsluiten van Control...")
        control.receiver.stop() 
