from dataclasses import dataclass as component

@component
class movable:
    def __init__(self, speed, init_direction):
        self.speed = speed
        self.base_speed = speed
        self.xshift = 0
        self.yshift = 0
        self.init_direction = init_direction
        self.direction = init_direction

@component
class accelerating:
    def __init__(self, acceleration, max_speed):
        self.acceleration = acceleration
        self.max_speed = max_speed

@component
class rotary:
    def __init__(self, original_image, angle_speed):
        self.original_image = original_image
        self.angle_speed = angle_speed
        self.current_angle_step = 0
        self.current_angle = 0

@component
class directional:
     def __init__(self, init_direction):
        self.init_direction = init_direction
        self.current_direction = init_direction