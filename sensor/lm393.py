# lm393_test.py

import time, csv
from gpiozero import DigitalInputDevice

class LM393SpeedSensor:
    def __init__(self, gpio_pin, openings=12):
        self.sensor = DigitalInputDevice(gpio_pin)
        self.openings = openings
        self.count = 0
        self.sensor.when_activated = self._count

    def _count(self):
        self.count += 1

    def get_rpm(self, duration):
        revolutions = self.count / self.openings
        rpm = (revolutions / duration) * 60
        return rpm

    def reset(self):
        self.count = 0

    def cleanup(self):
        self.sensor.close()

class RPMTest:
    def __init__(self):
        self.sensor1 = LM393SpeedSensor(gpio_pin=17)
        self.sensor2 = LM393SpeedSensor(gpio_pin=27)

    def run(self):
        with open("pwm_rpm_data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["PWM", "RPM_Left", "RPM_Right", "Delta"])

            for pwm in range(1801, 1600, -10):
                print(f"Testen met PWM: {pwm}")
                self.sensor1.reset()
                self.sensor2.reset()

                start_time = time.time()
                while time.time() - start_time < 5:
                    pass

                rpm1 = self.sensor1.get_rpm(5)
                rpm2 = self.sensor2.get_rpm(5)
                delta = rpm2 - rpm1

                print(f"PWM {pwm} → Left: {rpm1:.2f} RPM, Right: {rpm2:.2f} RPM, Delta: {delta:.2f}")
                writer.writerow([pwm, rpm1, rpm2, delta])

                time.sleep(1)

    def cleanup(self):
        self.sensor1.cleanup()
        self.sensor2.cleanup()
