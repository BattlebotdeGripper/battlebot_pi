import sys, os, time, struct

from regex import R
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.encoder import CANEncoder
from sensor.lm393 import RPMTest
from receiver.receiver_init import ReceiverInit

class Control:
    def __init__(self, serial: ReceiverInit = None, canbus: CANEncoder = None) -> None:
        self.canbus: CANEncoder | None = canbus
        self.receiver: ReceiverInit | None = serial

        self.rpmtest = RPMTest()
        self.wiel_omtrek: float = 39.269
        self.wielbasis: float = 49.0
        self.theta: float = 0.0
        self.delta: float = 0.0
        self.K_delta: float = 0.15
        self.K_theta: float = .0
        self.pwm_right_base = 0
        self.pwm_left_base = 0
        self.pwm_left_cal: float = -5
        self.pwm_right_cal: float = 0.0
        self.pwm_left: float = self.pwm_left_base + self.pwm_left_cal
        self.pwm_right: float = self.pwm_right_base + self.pwm_right_cal

    def run(self, mode: str = "straight") -> None:
        if self.receiver is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        if self.canbus is None:
            self.canbus = CANEncoder()
            self.canbus.callMCP2515Instance()

        print("Waiting for encoders to start...")
        if self.receiver is not None:
            while True:
                try:
                    data: int = self.receiver.read(32)

                    if len(data) < 32:
                        continue 

                    if data[0] == 0x20 and data[1] == 0x40 and len(data) == 32:
                        channels: Tuple[int, ...] = struct.unpack("<14H", data[2:30])
                        steering_data: Tuple[int, ...] = channels[:3]
                        print(steering_data)
                        self.pwm_left_base = steering_data[0]
                        self.pwm_right_base = steering_data[1]

                        self.rpm_left_sensor = self.rpmtest.sensor1.get_rpm(0.05)
                        self.rpm_right_sensor = self.rpmtest.sensor2.get_rpm(0.05)
                        self.delta = self.rpm_right_sensor - self.rpm_left_sensor

                        if mode == "straight":
                            pwm_adjust = (self.K_delta * self.delta) + (self.K_theta * self.theta)
                            self.pwm_left = self.pwm_left_base + self.pwm_left_cal - pwm_adjust
                            self.pwm_right = self.pwm_right_base + self.pwm_right_cal + pwm_adjust

                        self.canbus.sendSteering((int(self.pwm_left), int(self.pwm_right), 1500))

                        tijd_in_minuten = 0.05 / 60
                        afstand_left = (self.rpm_left_sensor * tijd_in_minuten) * self.wiel_omtrek
                        afstand_right = (self.rpm_right_sensor * tijd_in_minuten) * self.wiel_omtrek
                        delta_afstand = afstand_right - afstand_left
                        theta_rad = delta_afstand / self.wielbasis

                        self.theta += theta_rad

                    time.sleep(0.01)

                except KeyboardInterrupt:
                    print("KeyboardInterrupt detected, shutting down...")
                    self.stop_robot()
                    sys.exit(0)
                except Exception as e:
                    print(f"Error: {e}")
                    self.stop_robot()
                    time.sleep(0.5)

    def stop_robot(self):
        for _ in range(3):
            self.canbus.sendSteering((1500, 1500, 1500))
            time.sleep(0.1)

if __name__ == "__main__":

    receiver_init_instance = ReceiverInit()
    receiver = receiver_init_instance.getSerialConnection()
    
    control = Control(receiver)
    try:
        control.run(mode="straight")
    except KeyboardInterrupt:
        print("Main KeyboardInterrupt detected, shutting down...")
        control.stop_robot()
#        control.cleanup()
#        print("Cleaned up and exiting.")
        sys.exit(0)
#    finally:
#        control.cleanup()
