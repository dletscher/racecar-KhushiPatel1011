import random

class Agent:

    def chooseAction(self, observations, possibleActions):
        far_left, left, center, right, far_right = observations['lidar']
        vel = observations['velocity']

        # Steering Logic
        error_combined = (far_left + left) - (far_right + right)
        error_near = left - right

        a = 0.8
        b = 0.15
        error = a * error_combined + b * error_near

        c = 0.05
        if error > c:
            direction = 'left'
        elif error < -c:
            direction = 'right'
        else:
            direction = 'straight'

        # For Track 8
        spiral_turn = (center < 0.3 and left < 0.4 and right < 0.4) or (center < 0.25)
        distance = min(center, left, right) < 0.15

        # Speeding Logic
        if vel < 0.15:
            action_speed = 'accelerate'
        elif distance:
            action_speed = 'brake'
        elif spiral_turn:
            if vel > 0.17:
                action_speed = 'brake'
            else:
                action_speed = 'coast'
        else:
            base_brake = 3.0
            vel_factor = 7.5
            brake_threshold = base_brake + vel * vel_factor
            side_threshold = brake_threshold / 2.2

            if center < brake_threshold or left < side_threshold or right < side_threshold:
                action_speed = 'brake'
            elif vel < 1.0:
                action_speed = 'accelerate'
            else:
                action_speed = 'coast'

        return (direction, action_speed)

    def load(self, data=None):
        pass
