import can
from typing import Optional

class MCP2515:
    
    def __init__(self) -> None:
        self.channel: str = "can0"
        self.bustype: str = "socketcan"
        self.bus: Optional[can.BusABC] = None

    def initMcp2515(self) -> None:
        try:
            self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)

        except Exception as e:
            print(f"Kan niet de bus interface openen: {e}")
            self.bus = None

    def sendCanMessage(self, id, data) -> None:
        if self.bus:
            try:
                message: can.Message = can.Message(arbitration_id=id, data=data, is_extended_id=False)
                self.bus.send(message)

            except can.CanError:
                print("Er is iets fout gegaan met het configureren, bericht is niet verzonden!")
        else:
            print("CAN bus is niet geinitialiseerd. Kan bericht niet sturen.")

    def closeMcp2515(self) -> None:
        if self.bus:
            self.bus.shutdown()

    def receiveCanMessage(self) -> None:
        if self.bus:
            try:
                message: can.Message = self.bus.recv()
                print(f"Ontvangen: ID={hex(message.arbitration_id)}, Data={list(message.data)}")

            except can.CanError:  
                print("Er is iets fout gegaan bij het configureren van de bus, het bericht is niet ontvangen.")
        else:
            print("CAN bus niet geinitialiseerd. Kan bericht niet ontvangen.")
        pass