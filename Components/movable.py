from dataclasses import dataclass as component
from common.common import direction_vector

@component
class movable:
    def __init__(self, base_speed, init_direction, init_speed = 0):
        self.xspeed = init_speed
        self.yspeed = init_speed
        self.base_speed = base_speed
        self.xshift = 0
        self.yshift = 0
        self.init_direction = init_direction.copy()
        self.direction = direction_vector(init_direction)

@component
class accelerating:
    def __init__(self, acceleration, max_speed):
        self.xacceleration = 0
        self.yacceleration = 0
        self.max_speed = max_speed
        self.base_acceleration = acceleration

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
        self.base_direction = init_direction.copy()
        self.direction = init_direction.copy()
        self.move_up_dir = init_direction.copy()
        self.move_down_dir = init_direction.copy()