import can


class MCP2515:
    
    def __init__(self, channel = "can0", bustype = "socketcan"):
        self.channel = channel
        self.bustype = bustype
        self.bus = None

    def initMcp2515(self):
        try:
            self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)
            print(f"Verbonden met {self.bus} op channel {self.channel} with bustype {self.bustype}")

        except Exception as e:
            print(f"Kan niet de bus interface openen: {e}")
            self.bus = None

    def sendCanMessage(self, id, data):
        if self.bus:
            try:
                message = can.Message(arbitration_id=id, data=data, is_extended_id=False)
                self.bus.send(message)
                print("CAN-Bus bericht succesvol gestuurd!")

            except can.CanError:
                print("Something went wrong with the bus config and the message is not send")
        else:
            print("CAN bus is not initialized. Cannot send message.")

    def closeMcp2515(self):
        if self.bus:
            self.bus.shutdown()
            print("CAN bus gesloten")

    def receiveCanMessage(self):
        if self.bus:
            try:
                message = self.bus.recv()
                print(f"Received: ID={hex(message.arbitration_id)}, Data={list(message.data)}")

            except can.CanError:  
                print("Something went wrong with the bus config and the message is not receiving")
        else:
            print("CAN bus is not initialized. Cannot receive message.")
        pass