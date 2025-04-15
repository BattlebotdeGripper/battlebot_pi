import sys, os, time, csv, math
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.encoder import CANEncoder
from sensor.lm393 import RPMTest

class Control:
    def __init__(self, canbus: CANEncoder = None) -> None:
        self.canbus: CANEncoder | None = canbus
        self.rpmtest = RPMTest()
        self.wiel_omtrek: float = 39.269
        self.wielbasis: float = 49.0
        self.x: float = 0.0
        self.y: float = 0.0
        self.theta: float = 0.0
        self.K_delta: float = 0.15
        self.K_theta: float = .0
        self.pwm_base: int = 1700
        self.pwm_left_cal: float = -5
        self.pwm_right_cal: float = 0.0
        self.pwm_left: float = self.pwm_base + self.pwm_left_cal
        self.pwm_right: float = self.pwm_base + self.pwm_right_cal
        self.running: bool = False
        self.run_number: int = 0
        self.start_time: float = 0.0  # Voor timeout

    def run(self, mode: str = "straight", target_distance: float = 200.0, max_run_time: float = 30.0) -> None:
        if self.canbus is None:
            self.canbus = CANEncoder()
            self.canbus.callMCP2515Instance()

        print("Waiting for encoders to start...")
        timeout = 10.0  # Max 10 seconden wachten op encoders
        start_wait = time.time()
        while True:
            try:
                if self.canbus.checkEncoders() and not self.running:
                    self.run_number += 1
                    self.running = True
                    self.start_time = time.time()
                    print(f"\nRun {self.run_number} ({mode.capitalize()} Mode - Target: {target_distance} cm)\n{'=' * 10}")
                    with open(f"pwm_rpm_data_run_{self.run_number}.csv", mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Timestamp", "PWM_Left", "PWM_R", "RPM_L", "RPM_R",
                                       "Delta", "Afstand_L", "Afstand_R", "X", "Y", "Theta_deg"])

                        self.x, self.y, self.theta = 0.0, 0.0, 0.0
                        time.sleep(0.2)
                        self.pwm_left = self.pwm_base + self.pwm_left_cal
                        self.pwm_right = self.pwm_base + self.pwm_right_cal

                        while self.x < target_distance:
                            if time.time() - self.start_time > max_run_time:
                                print("Max run time exceeded, forcing stop...")
                                self.stop_robot()
                                break

                            self.rpmtest.sensor1.reset()
                            self.rpmtest.sensor2.reset()
                            time.sleep(0.05)

                            rpm_left = self.rpmtest.sensor1.get_rpm(0.05)
                            rpm_right = self.rpmtest.sensor2.get_rpm(0.05)
                            delta = rpm_right - rpm_left

                            if mode == "straight":
                                pwm_adjust = (self.K_delta * delta) + (self.K_theta * self.theta)
                                self.pwm_left = self.pwm_base + self.pwm_left_cal - pwm_adjust
                                self.pwm_right = self.pwm_base + self.pwm_right_cal + pwm_adjust

                            self.pwm_left = max(1500, min(1800, self.pwm_left))
                            self.pwm_right = max(1500, min(1800, self.pwm_right))
                            self.canbus.sendSteering((int(self.pwm_left), int(self.pwm_right), 1500))

                            tijd_in_minuten = 0.05 / 60
                            afstand_left = (rpm_left * tijd_in_minuten) * self.wiel_omtrek
                            afstand_right = (rpm_right * tijd_in_minuten) * self.wiel_omtrek
                            afstand_gem = (afstand_left + afstand_right) / 2
                            delta_afstand = afstand_right - afstand_left
                            theta_rad = delta_afstand / self.wielbasis

                            self.theta += theta_rad
                            theta_deg = math.degrees(self.theta)
                            next_x = self.x + (afstand_gem * math.cos(self.theta))
                            self.y += afstand_gem * math.sin(self.theta)

                            if next_x >= target_distance:
                                overshoot = next_x - target_distance
                                afstand_gem -= overshoot
                                self.x = target_distance
                            else:
                                self.x = next_x

                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                            writer.writerow([
                                timestamp, round(self.pwm_left, 1), round(self.pwm_right, 1),
                                round(rpm_left, 1), round(rpm_right, 1), round(delta, 1),
                                round(afstand_left, 1), round(afstand_right, 1),
                                round(self.x, 1), round(self.y, 1), round(theta_deg, 1)
                            ])
                            print(f"Run {self.run_number} - Left: {rpm_left:.1f}, Right: {rpm_right:.1f}, "
                                  f"Delta: {delta:.1f}, PWM_L: {self.pwm_left:.1f}, PWM_R: {self.pwm_right:.1f}, "
                                  f"X: {self.x:.1f}, Y: {self.y:.1f}, Theta: {theta_deg:.1f}°")

                            if self.x >= target_distance:
                                self.stop_robot()
                                print(f"Run {self.run_number} completed. Distance reached: {self.x:.1f} cm\n{'=' * 10}")
                                self.running = False
                                break

                        break
                elif time.time() - start_wait > timeout:
                    print("Timeout waiting for encoders, forcing cleanup...")
#                    self.cleanup()
                    sys.exit(1)
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("KeyboardInterrupt detected, shutting down...")
                self.stop_robot()
#                self.cleanup()
                print("Cleaned up and exiting.")
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}")
                self.stop_robot()
                time.sleep(0.5)

    def stop_robot(self):
        """Forceer stop van de robot met meerdere pogingen."""
        for _ in range(3):  # Probeer 3 keer om zeker te zijn
            self.canbus.sendSteering((1500, 1500, 1500))
            time.sleep(0.1)

#    def cleanup(self):
#        print("Starting cleanup...")
#        self.rpmtest.cleanup()
#        if self.canbus:
#            self.canbus.cleanup()
#        print("Cleanup completed.")

if __name__ == "__main__":
    control = Control()
    try:
        control.run(mode="straight", target_distance=10000000.0, max_run_time=30.0)
    except KeyboardInterrupt:
        print("Main KeyboardInterrupt detected, shutting down...")
        control.stop_robot()
#        control.cleanup()
#        print("Cleaned up and exiting.")
        sys.exit(0)
#    finally:
#        control.cleanup()

