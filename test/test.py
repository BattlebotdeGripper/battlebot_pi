# steering_data = (1478, 1139, 1000)

# def difference_wheels_pwm(steering_data):
#     wiel_a = steering_data[0]
#     wiel_b = steering_data[1]
#     gripper = steering_data[2]

#     min_waarde_wiel = min(wiel_a, wiel_b)
#     max_waarde_wiel = max(wiel_a, wiel_b)

#     difference_values = int((max_waarde_wiel % min_waarde_wiel) / 2)
    
#     if wiel_a > wiel_b:
#         wiel_a -= difference_values 
#         wiel_b += difference_values
#     elif wiel_a < wiel_b:
#         wiel_a += difference_values
#         wiel_b -= difference_values 
#     # self.canbus.sendSteering()
#     print(wiel_a, wiel_b)
#     return wiel_a, wiel_b, gripper

# difference_wheels_pwm(steering_data)

