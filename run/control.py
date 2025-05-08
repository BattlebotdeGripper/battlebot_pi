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
        # self.left_sensor = LM393SpeedSensor(gpio_pin=17)
        # self.right_sensor = LM393SpeedSensor(gpio_pin=27)
        self.buffer = b""  # Buffer voor asynchrone data
        # Correctiefactoren voor motoren (aanpassen na kalibratie)
        self.left_motor_correction = 1.0  # Vermenigvuldigfactor voor linker motor
        self.right_motor_correction = 0.99  # Vermenigvuldigfactor voor rechter motor

    def process_data(self, data: bytes) -> None:
        """Verwerk ontvangen data, zoals in de originele run-methode."""
        self.buffer += data
        while len(self.buffer) >= 32:
            if self.buffer[0] == 0x20 and self.buffer[1] == 0x40:
                try:
                    channels: Tuple[int, ...] = struct.unpack("<14H", self.buffer[2:30])
                    corrigerende_tik_links = -5
                    corrigerende_tik_rechts = 0
                    gripper = channels[2]
                    links = channels[0]
                    rechts = channels[1]

                    # Detecteer rechtdoor rijden (wanneer links en rechts ongeveer gelijk zijn)
                    threshold = 50  # Tolerantie voor 'gelijke' stuurwaarden
                    if abs(links - rechts) <= threshold:
                        # Pas correctiefactoren toe voor rechtdoor rijden
                        adjusted_links = int(links * self.left_motor_correction) + corrigerende_tik_links
                        adjusted_rechts = int(rechts * self.right_motor_correction) + corrigerende_tik_rechts
                        # Beperk waarden tot geldige PWM-bereik (1000-2000)
                        adjusted_links = max(1000, min(2000, adjusted_links))
                        adjusted_rechts = max(1000, min(2000, adjusted_rechts))
                    else:
                        # Geen correctie voor bochten (voor nu)
                        adjusted_links = links + corrigerende_tik_links
                        adjusted_rechts = rechts + corrigerende_tik_rechts
                        adjusted_links = max(1000, min(2000, adjusted_links))
                        adjusted_rechts = max(1000, min(2000, adjusted_rechts))

                    steering_data = (adjusted_links, adjusted_rechts, gripper)
                    print(f"Stuurdata: {steering_data}")
                    self.canbus.sendHeartbeat()
                    self.canbus.sendSteering(steering_data)
                except Exception as e:
                    print(f"Fout bij verwerken van iBUS data: {e}")
                    if self.canbus:
                        self.canbus.triggerFailsafe()
            else:
                print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                # Schuif buffer op om te zoeken naar nieuwe header
                self.buffer = self.buffer[1:]
                continue
            self.buffer = self.buffer[32:]  # Verwijder verwerkte data

if __name__ == "__main__":
    try:
        receiver_init_instance = ReceiverInit()
        serial_connection = receiver_init_instance.getSerialConnection()
        canbus_instance = CANEncoder()
        canbus = canbus_instance.callMCP2515Instance()

        controller = Control(serial_connection, canbus)

        # Haal poort en baudrate uit de seriële verbinding
        serial_port = serial_connection.port
        baudrate = serial_connection.baudrate

        # Start de asynchrone loop
        asyncio.run(run_control(serial_port, baudrate, controller))
    except Exception as e:
        print(f"Error: {e}")