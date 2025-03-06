# from test_led import Led

class Control:
    def __init__(self):
        # self.leds = Led()
        pass

    def run(self, channel_values):        
        # while True:
            # channel_values = Receiver.readData()
            # print(channel_values)
        if channel_values:
            print(f"{channel_values}")
            # Leds.controlLeds(channel_values)
            pass

if __name__ == "__main__":
    pass
    # call_control = Control()