from mcp2515 import MCP2515
from time import sleep

class Control:
    def __init__(self):
        self.mcp2515 = MCP2515()

    def run(self, data):   
        try:            
            self.mcp2515.initMcp2515()
            # while True:

            if data["can_id"] == 100:
                print(f"{data}")
                self.mcp2515.sendCanMessage(data["can_id"], data["data"])
            sleep(0.1) 
        finally:
            self.mcp2515.closeMcp2515()     
            
if __name__ == "__main__":
    call_control = Control()
    call_control.run()
