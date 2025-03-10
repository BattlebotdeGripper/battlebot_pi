import struct
from control import Control
from receiver_init import ReceiverInit
import time
from mcp2515 import MCP2515

class ReceiverData:
    def __init__(self, serial: ReceiverInit, control: Control, mcp2515: MCP2515):
        self.serial = serial
        self.serial_init = self.serial.getSerialConnection()
        self.control = control
        self.mcp2515 = mcp2515

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
                    # self.control.run(channels)
                    # print(channels)

                    self.setCanMessages(channels)

                else:
                    print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    self.serial.reset_input_buffer()

                time.sleep(0.001)

            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                self.serial.reset_input_buffer()
                time.sleep(1) 

    def setCanMessages(self, channels):
        """
        # 
        # Total values bytes steering: 100 15 00 15 00 15 00 00 00
        # First number: 100 CAN_ID
        # First 2 bytes are for wheel A: 15 00  
        # Second 2 bytes are for wheel B: 15 00
        # Third 2 bytes are for gripper: 15 00
        # Fourth 2 bytes are for debug: 00 00
        #  
        """

        wheel_a = str(channels[0])
        wheel_a_first_byte = wheel_a[0:2]
        wheel_a_second_byte = wheel_a[2:4]

        # De code ":02d" zorgt ervoor dat er ten alle tijden 2 getallen blijven staan
        wheel_a_dict = {
            "can_id": 100,
            "data": [
                        int(wheel_a_first_byte), 
                        # f"{int(wheel_a_second_byte):02d}"
                        int(wheel_a_second_byte)
                    ]
        }

        # print(wheel_a_dict)
        self.control.run(wheel_a_dict)

if __name__ == "__main__":
    receiver_init_instance = ReceiverInit()
    receiver_init_instance.setUpSerialConnection()
    
    control_init_instance = Control()
    mcp2515_init_instance = MCP2515()

    try:
        get_ibus_data = ReceiverData(receiver_init_instance, control_init_instance, mcp2515_init_instance)
        channels = get_ibus_data.readData()
    except Exception as e:
        print(f"Error: {e}")
