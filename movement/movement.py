from gpiozero import PWMOutputDevice
import time

class Movement:
    def __init__(self, pins):
        self.min_duty = 1000
        self.neutral = 1500
        self.max_duty = 2000
        self.esc = [PWMOutputDevice(pin, frequency=50) for pin in pins] 
        self.setup_esc()

    def _us_to_duty(self, us):
        return (us - self.min_duty) / (self.max_duty - self.min_duty)

    def setup_esc(self):
        for i in range(len(self.esc)):
            self.esc[i].value = self._us_to_duty(self.neutral)
            time.sleep(0.1)

    def move(self, duty_cycles):
        for i in range(len(self.esc)):
            duty = duty_cycles[i]

            if self.min_duty <= duty <= self.max_duty:
                self.esc[i].value = self._us_to_duty(duty)
