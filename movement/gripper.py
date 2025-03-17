from movement.movement import Movement

class Gripper(Movement):

    # max_duty = 2000
    # min_duty = 1000
    # neutral = 1500

    def __init__(self):
        super().__init__(pins=[18])

    def run(self, gripper_value):
        gripper_value = max(min(gripper_value, self.max_duty), self.min_duty)