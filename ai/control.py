import sys, os, time, csv, math
from datetime import datetime  # Import datetime to get the current time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.encoder import CANEncoder
from sensor.lm393 import LM393SpeedSensor, RPMTest

class Control:
    def __init__(self, canbus: CANEncoder = None) -> None:
        self.canbus: CANEncoder | None = canbus
        self.rpmtest = RPMTest()

    def run(self) -> None:
        if self.canbus is None:
            self.canbus = CANEncoder()
            self.canbus.callMCP2515Instance()

        while True:
            try:
                if self.canbus.checkEncoders():
                    print("Start time reached. Starting RPM test.")
                    # Open CSV and write headers
                    with open("pwm_rpm_data.csv", mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Timestamp", "PWM", "RPM_Left", "RPM_Right", "Delta"])
                        
                        # Iterate through each PWM value and test
                        for pwm in range(1800, 1599, -10):  # Adjusted to match Pico's range
                            print(f"Testing PWM: {pwm}")
                            # Send PWM to Pico via CAN (0x100 message)
                            self.canbus.sendSteering((pwm, pwm, 1500))  # Using 1500 as a neutral third value
                            
                            # Reset sensor counters and wait for RPM measurement
                            self.rpmtest.sensor1.reset()
                            self.rpmtest.sensor2.reset()
                            time.sleep(5)  # Allow motors to stabilize and measure over 5 seconds
                            
                            # Calculate RPM
                            rpm_left = self.rpmtest.sensor1.get_rpm(5)
                            rpm_right = self.rpmtest.sensor2.get_rpm(5)
                            delta = rpm_right - rpm_left
                            
                            # Get the current timestamp
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format as "YYYY-MM-DD HH:MM:SS"
                            
                            # Write data to CSV
                            writer.writerow([
                                timestamp, 
                                math.floor(pwm * 10) / 10, 
                                math.floor(rpm_left * 10) / 10, 
                                math.floor(rpm_right * 10) / 10, 
                                math.floor(delta * 10) / 10
                            ])
                            print(f"PWM {pwm} → Left: {rpm_left:.2f}, Right: {rpm_right:.2f}, Delta: {delta:.2f}")
                    self.canbus.sendSteering((1500, 1500, 1500)) 
                    break  # Exit after test
                time.sleep(0.5)
            except Exception as e:
                self.canbus.sendSteering((1500, 1500, 1500)) 
                print(f"Error: {e}")
                time.sleep(0.5)

    def cleanup(self):
        self.rpmtest.cleanup()

if __name__ == "__main__":
    control = Control()
    try:
        control.run()
    except KeyboardInterrupt:
        control.canbus.sendSteering((1500, 1500, 1500)) 
        print("Interrupted.")
    finally:
        control.cleanup()
