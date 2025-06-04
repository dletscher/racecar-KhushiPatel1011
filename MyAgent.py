import random

class Agent:

    def chooseAction(self, observations, possibleActions):
        far_left, near_left, center, near_right, far_right = observations['lidar']
        vel = observations['velocity']

        # STEERING LOGIC
        error_combined = (far_left + near_left) - (far_right + near_right)
        error_near = near_left - near_right

        # Weighted sum: a for combined, b for near
        a = 0.3
        b = 0.7
        error = a * error_combined + b * error_near

        # Dead‐zone Threshold (Smaller Threshold)
        c = 0.1

        if error > c:
            direction = 'left'
        elif error < -c:
            direction = 'right'
        else:
            direction = 'straight'

        # SPEED LOGIC
        if vel < 0.2:
            # Starting Acceleration
            action_speed = 'accelerate'
        else:
            # Dynamic Brake Thresholds
            base_brake = 4.0
            vel_factor = 8.0
            brake_threshold = base_brake + vel * vel_factor
            side_threshold = brake_threshold / 2.0

            # BRACKING AND ACCELERATING LOGIC
            if center < brake_threshold or near_left < side_threshold or near_right < side_threshold:
                action_speed = 'brake'
            else:
                if vel < 1.0:
                    action_speed = 'accelerate'
                else:
                    action_speed = 'coast'

        return (direction, action_speed)

    def load(self, data=None):
        pass

