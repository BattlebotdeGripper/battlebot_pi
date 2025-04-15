import sys, os, time, struct

from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from receiver.receiver_init import ReceiverInit
from mcp.encoder import CANEncoder

class Control:
    def __init__(self, serial: ReceiverInit = None, canbus: CANEncoder = None) -> None:
        self.serial: ReceiverInit | None = serial
        self.canbus: CANEncoder | None = canbus

    def run(self) -> None:
        # Als er geen UART verbinding met de Receiver is, maak verbinding dan
        if self.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return
        
        # Als er geen CAN verbinding met de MCP2515 is, maak verbinding dan
        if self.canbus is None:
            self.canbus: CANEncoder = CANEncoder()
            self.canbus.callMCP2515Instance()

        while True:
            try:
                # Haal de serieele data op van de Fly-Sky Receiver
                data: int = self.serial.read(32)

                # Zorgt ervoor dat de data pas wordt opgehaald als de volledig aantal bytes beschikbaar is
                if len(data) < 32:
                    continue 

                data: int = self.serial.read(32)

                # Kijkt naar de headers en de verwachte lengte
                # 
                # 0x20 - header dat het een commando pakket is
                # 0x40 - lengte-indicator van het pakket 32 bytes
                # len(data) - bevestiging van lengte
                #
                if data[0] == 0x20 and data[1] == 0x40 and len(data) == 32:

                    # De data die nodig is
                    #
                    # [2:30] - Pak de bytes 2 t/m 29 (14 waardes, 2 bytes ieder)
                    # 14H - decodeert 14 channelwaardes naar unsigned short
                    # 
                    channels: Tuple[int, ...] = struct.unpack("<14H", data[2:30])

                    # Pak alleen eerste 3 channels en stuur door naar de method sendSteerin()
                    #
                    # (channel 1) - linkerwiel
                    # (channel 2) - rechterwiel
                    # (channel 3) - grijparm
                    # print(channels)
                    steering_data: Tuple[int, ...] = channels[:3]
                    print(steering_data)

                    self.canbus.sendSteering(steering_data)

                else:
                    print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    self.serial.reset_input_buffer()

                # De snelheid van data verbinden. LET OP: Belangrijk voor CPU!
                time.sleep(0.01)

            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                self.serial.reset_input_buffer()
                time.sleep(0.5)
                

receiver_init_instance = ReceiverInit()
receiver = receiver_init_instance.getSerialConnection()

canbus_encoder_instance = CANEncoder()
canbus_mcp2515_instance = canbus_encoder_instance.callMCP2515Instance()

get_ibus_data = Control(receiver, canbus_mcp2515_instance)

try:
    channels = get_ibus_data.run()
except Exception as e:
    print(f"Error: {e}")
