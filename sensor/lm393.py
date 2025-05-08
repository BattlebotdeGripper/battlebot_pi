from gpiozero import DigitalInputDevice
import time

class LM393SpeedSensor:
    def __init__(self, gpio_pin: int, openings: int = 12):
        self.sensor = DigitalInputDevice(gpio_pin)
        self.openings = openings
        self.count = 0
        self.last_time = time.time()
        self.sensor.when_activated = self._count

    def _count(self):
        self.count += 1

    def get_rpm(self, duration: float = 0.1) -> float:
        current_time = time.time()
        elapsed = current_time - self.last_time
        if elapsed >= duration:
            revolutions = self.count / self.openings
            rpm = (revolutions / elapsed) * 60
            self.count = 0
            self.last_time = current_time
            return rpm
        return 0.0

    def reset(self):
        self.count = 0
        self.last_time = time.time()

    def cleanup(self):
        self.sensor.close()