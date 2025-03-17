import time
from receiver.receiver import ReceiverData
from movement.drive import Drive
from movement.gripper import Gripper

class Control:

    # pin=16 - Linkerwiel - channel=1
    # pin=17 - Rechterwiel - channel=2

    def __init__(self):
        self.receiver = ReceiverData()
        self.receiver.callReceiverInit()
        self.receiver.start()
        self.drive = Drive()
        self.gripper = Gripper()

    def run(self):
        while True:
            data = self.receiver.getLatestData()
            if data:
                print(data)
                str_data = f"{data}\n"
                # print(f"3 channels: {str_data}")
                try:
                    linkerwiel, rechterwiel = int(data[0]), int(data[1])
                    gripper = int(data[2])

                    self.drive.run(linkerwiel, rechterwiel)
                    self.gripper.run(gripper)

                    # linkerwiel, rechterwiel, gripper_value = map(int, data.split(","))
                    # self.drive.run(linkerwiel, rechterwiel)
                    # self.gripper.run(gripper_value)
                except ValueError:
                    print("Geen geldige data ontvangen!")
            time.sleep(0.01) # Deze kan veranderd worden om een snellere verbinding te krijgen!

    # def start(self):
    #     self.run() 

if __name__ == "__main__":
    control = Control()

    try:
        control.run() 
    except KeyboardInterrupt:
        print("\nAfsluiten van Control...")
        # control.receiver.stop() 