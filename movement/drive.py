from movement.movement import Movement

class Drive(Movement):

    # max_duty = 2000
    # min_duty = 1000
    # neutral = 1500

    def __init__(self):
        super().__init__(pins=[26, 27])
        
    def moveForward(self, wheel_a, wheel_b):
        self.move([wheel_a, wheel_b]) 
        print("Moving forward")

    def moveBackwards(self, wheel_a, wheel_b):
        self.move([wheel_a, wheel_b]) 
        print("Moving backwards")

    def turnRight(self, wheel_a, wheel_b):
        self.move([wheel_a, wheel_b]) 
        print("Turning right")

    def turnLeft(self, wheel_a, wheel_b):
        self.move([wheel_a, wheel_b]) 
        print("Turning left")

    def run(self, wheel_a, wheel_b):
        wheel_a = max(min(wheel_a, self.max_duty), self.min_duty)
        wheel_b = max(min(wheel_b, self.max_duty), self.min_duty)

        if wheel_a > self.neutral and wheel_b > self.neutral:
            self.moveForward(wheel_a, wheel_b)
        elif wheel_a < self.neutral and wheel_b < self.neutral:
            self.moveBackwards(wheel_a, wheel_b)
        elif wheel_a > wheel_b:
            self.turnRight(wheel_a, wheel_b)
        elif wheel_a < wheel_b:
            self.turnLeft(wheel_a, wheel_b)