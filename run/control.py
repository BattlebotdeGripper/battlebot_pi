import sys, os, time, struct, asyncio
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from receiver.receiver_init import ReceiverInit
from mcp.encoder import CANEncoder
from sensor.lm393 import LM393SpeedSensor
from receiver.receiver_async import run_control

class Control:
    def __init__(self, serial, canbus: CANEncoder = None) -> None:
        self.serial = serial
        self.canbus = canbus
        
        # self.right_sensor = LM393SpeedSensor(gpio_pin=17)
        # self.left_sensor = LM393SpeedSensor(gpio_pin=18)

        self.buffer = b""
        self.treshold = 50
    def calculate_differrence(self, wiel_a, wiel_b):
        min_waarde_wiel = min(wiel_a, wiel_b)
        max_waarde_wiel = max(wiel_a, wiel_b)

        difference_values = int((max_waarde_wiel % min_waarde_wiel) / 2)
        print(f"Verschil {difference_values}")
        return difference_values

    def difference_wheels_pwm(self, steering_data):
        wiel_a = steering_data[0]
        wiel_b = steering_data[1]
        gripper = steering_data[2]

        difference_values = self.calculate_differrence(wiel_a, wiel_b)

        if wiel_a > wiel_b:
            wiel_a -= difference_values 
            wiel_b += difference_values
        elif wiel_a < wiel_b:
            wiel_a += difference_values
            wiel_b -= difference_values 

        return wiel_a, wiel_b, gripper    

    def process_data(self, data: bytes) -> None:
        self.buffer += data
        while len(self.buffer) >= 32:
            if self.buffer[0] == 0x20 and self.buffer[1] == 0x40:
                try:
                    channels: Tuple[int, ...] = struct.unpack("<14H", self.buffer[2:30])
                    gripper = channels[2]
                    links = channels[0]
                    rechts = channels[1]

                    steering_data = (links, rechts, gripper)

                    difference = self.calculate_differrence(links, rechts)

                    # print(steering_data)
                    if difference < (self.treshold + 10):

                        adjust_links, adjust_rechts, adjust_gripper = self.difference_wheels_pwm(steering_data)

                    # Zorg ervoor dat de wielen even hard draaien
                        if adjust_links >= 1625:
                            adjust_rechts += self.treshold
                            # print(adjust_links)
                            if adjust_rechts >= 2000:
                                adjust_rechts = 2000

                        tuple_data = (adjust_links, adjust_rechts, adjust_gripper)

                        print(f"Stuurdata: {tuple_data}")

                        self.canbus.sendSteering(tuple_data)
                    else:
                        self.canbus.sendSteering(steering_data)
                    self.canbus.sendHeartbeat()

                except Exception as e:
                    print(f"Fout bij verwerken van iBUS data: {e}")
                    if self.canbus:
                        self.canbus.triggerFailsafe()
            else:
                print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                self.buffer = self.buffer[1:]
                continue
            self.buffer = self.buffer[32:]

if __name__ == "__main__":
    try:
        receiver_init_instance = ReceiverInit()
        serial_connection = receiver_init_instance.getSerialConnection()
        canbus_instance = CANEncoder()
        canbus = canbus_instance.callMCP2515Instance()

        controller = Control(serial_connection, canbus)

        serial_port = serial_connection.port
        baudrate = serial_connection.baudrate

        asyncio.run(run_control(serial_port, baudrate, controller))
    except Exception as e:
        print(f"Error: {e}")
