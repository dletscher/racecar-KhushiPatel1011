import random

class Agent:

    def chooseAction(self, observations, possibleActions):
        lidar = observations['lidar']
        velocity = observations['velocity']

        # Replacing infinity distance factor with a large static number that is 100 for easier calculations
        lidar = [d if d != float('inf') else 100.0 for d in lidar] 
        far_left, left, center, right, far_right = lidar

        side_diff = (far_left + left) - (far_right + right)
        near_diff = left - right

        # Weight Errors for side diff and near diff
        a = 0.7
        b = 0.3
        error = a * side_diff + b * near_diff

        # Controls for deciding which action to take
        if error > 0.05:
            direction = 'left'
        elif error < -0.05:
            direction = 'right'
        else:
            direction = 'straight'

        # Speeding Logic with breakdows of path
        min_front = min(left, center, right)
        min_side = min(far_left, far_right)
        curvature = (left + right) - (far_left + far_right)
        
        safe_velocity = 0.12

        # Condition for braking 
        if center < 0.12 or min_front < 0.12 or min_side < 0.12:
            speed_action = 'brake'

        # Sharp Turn within safe velocity => coast
        elif (min_front < 0.25 or abs(error) > 2.2) and velocity > 0.08:
            speed_action = 'coast'

        # If car is very slow than the safe velocity => accelerate
        elif velocity < 0.05 and center > 0.2 and min_side > 0.2:
            speed_action = 'accelerate'

        # If car is moving above the safe velocity => coast
        elif velocity >= safe_velocity:
            speed_action = 'coast'

        # Condition other than that, agent always needs to accelerate
        else:
            speed_action = 'accelerate'

        return (direction, speed_action)
