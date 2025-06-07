import random

class Agent:

    def chooseAction(self, observations, possibleActions):
        lidar = observations['lidar']
        velocity = observations['velocity']
       
        lidar = [d if d != float('inf') else 100.0 for d in lidar]
        far_left, left, center, right, far_right = lidar

        # Steering Logic
        side_diff = (far_left + left) - (far_right + right)
        near_diff = left - right
       
        # Weighted sum
        a = 0.6 # for side diff
        b = 0.4 # for near diff
        error = 0.6 * side_diff + 0.4 * near_diff

        # Small Threshold
        c = 0.1

        if error > c:
            direction = 'left'
        elif error < -c:
            direction = 'right'
        else:
            direction = 'straight'
           
        min_front = min(left, center, right)
        min_side = min(far_left, far_right)
        curvature = (left + right) - (far_left + far_right)

        # Apply brake only if car is very close to crashing into side lanes
        if center < 0.06 or min_front < 0.05:
            speed_action = 'brake'

        # If the curve is sharp and the car is fast => only coast
        elif (min_front < 0.2 or abs(error) > 1.8) and velocity > 0.12:
            speed_action = 'coast'

        # If the car is slow => accelerate
        elif velocity < 0.2:
            speed_action = 'accelerate'

        # Always accelerate when there is clear straight track
        else:
            speed_action = 'accelerate'

        return (direction, speed_action)
