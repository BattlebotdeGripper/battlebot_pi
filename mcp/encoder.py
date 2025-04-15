from typing import Tuple, List
from mcp.mcp2515 import MCP2515
from datetime import datetime, timedelta

class CANEncoder:

    def __init__(self) -> None:
        self.mcp2515: MCP2515 | None = None
        self.start_time = datetime.now()

    def callMCP2515Instance(self) -> "CANEncoder":
        if self.mcp2515 is None:
            # print("@@@@@@@@@@@@@@@@@@")
            self.mcp2515 = MCP2515()
            self.mcp2515.initMcp2515()
        return self

    def sendSteering(self, steering_channels: Tuple[int, ...]):
        
        if self.mcp2515 is None:
            print("MCP2515 instantie niet geïnitialiseerd")
            return

        can_id: int = 0x100
        data: List[int] = []

        for value in steering_channels:
        
            # Verdeel elke 16-bit waarde van iBUS stuurkanalen in twee 8-bit bytes (big-endian).
            # In iBUS zijn kanaalwaarden 16-bit integers, bijv. 1500 (0x05DC in hex). 
            # Omdat een CAN-bus maximaal 8 bytes per bericht ondersteunt, moeten we elk kanaal 
            # opdelen in twee afzonderlijke bytes: een high byte en een low byte.
            #
            # Voorbeeld: 
            #     value = 1500 = 0x05DC = 00000101 11011100 (in binaire 16 bits)
            #
            # (value >> 8) verschuift de bits 8 posities naar rechts:
            #     00000101 11011100  →  00000000 00000101  → high byte (0x05)
            #
            # value & 0xFF haalt de onderste 8 bits eruit - & = bitwise AND:
            #     00000101 11011100  &  00000000 11111111  = 11011100  → low byte (0xDC)
            #
            # Resultaat:
            #     high = 0x05
            #     low  = 0xDC
            #
            # Deze worden toegevoegd aan een CAN-data array, zodat we de stuurinformatie 
            # byte-per-byte kunnen versturen via de CAN-bus.
            high: int = (value >> 8) & 0xFF
            low: int = value & 0xFF

            data.append(high)
            data.append(low)

        print(f"CAN-data: {can_id:03X} [{len(data)}] {' '.join(f'{b:02X}' for b in data)}")

        self.mcp2515.sendCanMessage(can_id, data)

    def triggerFailsafe(self) -> None:
        pass

    def sendHeartbeat(self) -> None:
        pass

    def checkEncoders(self) -> bool:
        if self.mcp2515 is None:
            print("MCP2515 instantie niet geïnitialiseerd")
            return False

        now = datetime.now()
        if now >= self.start_time + timedelta(seconds=5):
            print("20 seconden verstreken, start signaal verzenden via CAN!")
            # can_id: int = 0x200
            # data = [0x01]
            # self.mcp2515.sendCanMessage(can_id, data)
            return True

        return False

