import lgpio
import time

class Sensors:
    def __init__(self, forward_trigger=24, forward_echo=23, gpio_chip=0):
        self.forward_trigger = forward_trigger
        self.forward_echo = forward_echo
        # back_trigger=27, back_echo=22
        # self.back_trigger = back_trigger
        # self.back_echo = back_echo
        self.gpio = lgpio.gpiochip_open(gpio_chip)

    def setup_sensors(self):    
        lgpio.gpio_claim_output(self.gpio, self.forward_trigger)
        lgpio.gpio_claim_input(self.gpio, self.forward_echo)
        # lgpio.gpio_claim_output(self.gpio, self.back_trigger)
        # lgpio.gpio_claim_input(self.gpio, self.back_echo)

    def measure_distance(self, trigger, echo):
        lgpio.gpio_write(self.gpio, trigger, 1)
        time.sleep(0.00001)
        lgpio.gpio_write(self.gpio, trigger, 0)

        while lgpio.gpio_read(self.gpio, echo) == 0:
            pass
        start_time = time.time()

        while lgpio.gpio_read(self.gpio, echo) == 1:
            pass
        end_time = time.time()

        return (end_time - start_time) * 17150

    def gpio_stop(self):
        for pin in [self.forward_trigger, self.forward_echo]:
            # , self.back_trigger, self.back_echo
            lgpio.gpio_release(self.gpio, pin)
        lgpio.gpiochip_close(self.gpio)

    def run(self):
        self.setup_sensors()
        try:
            while True:
                print(f"Sensor 1: {self.measure_distance(self.forward_trigger, self.forward_echo):.2f} cm")
                # print(f"Sensor 2: {self.measure_distance(self.back_trigger, self.back_echo):.2f} cm")
                time.sleep(1)
        except KeyboardInterrupt:
            print("The scripts has been interrupted")
            pass
        finally:
            self.gpio_stop()


if __name__ == "__main__":
    try:
        sensor = Sensors()
        sensor.run()
    except KeyboardInterrupt:
        print("Interrupted")