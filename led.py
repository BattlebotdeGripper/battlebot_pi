from mcp2515 import MCP2515

class Led:
    
    def __init__(self, mcp2515, id=0x200, data=[0x00]):
        self.id = id
        self.data = data
        self.mcp2515 = mcp2515

    def set_led_on(self):
        self.data = [0x01]
        self.mcp2515.send_can_message(self.id, self.data)
        print("Led is nu aan")

    
    def set_led_off(self):
        self.data = [0x00]
        self.mcp2515.send_can_message(self.id, self.data)
        print("Led is nu uit")


