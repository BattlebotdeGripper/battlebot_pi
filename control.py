from mcp2515 import MCP2515
from time import sleep

class Control:
    def __init__(self):
        self.mcp2515 = MCP2515()

    def run(self):   
        try:            
            self.mcp2515.init_mcp2515()
            while True:
                pass

        finally:
            self.mcp2515.close_mcp2515()     
            
if __name__ == "__main__":
    call_control = Control()
    call_control.run()