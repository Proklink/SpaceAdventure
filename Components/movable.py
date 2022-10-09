from dataclasses import dataclass as component

@component
class movable:
    def __init__(self, speed):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.speed = speed

@component
class accelerating:
    def __init__(self, acceleration, max_speed):
        self.acceleration = acceleration
        self.max_speed = max_speed

@component
class rotary:
    def __init__(self, original_image, angle_speed, init_direction):
        self.moving_right = False
        self.moving_left = False

        self.original_image = original_image
        self.angle_speed = angle_speed
        self.current_angle = 0
        self.init_direction = init_direction
        self.current_direction = init_direction