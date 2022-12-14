from ecs.ECS import Processor
from Components.movable import accelerating, movable, rotary, directional

class PlayerController(Processor):
    def __init__(self, id, bullet_generator):
        super().__init__()
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.rotate_right = False
        self.rotate_left = False

        self.shooting = False
        self.player_id = id

        self.frames_per_bullet = 20
        self.frames = 0

        self.add_bullet = bullet_generator

    def right_flag(self, flag):
        self.moving_right = flag
    def left_flag(self, flag):
        self.moving_left = flag
    def up_flag(self, flag):
        self.moving_up = flag
    def down_flag(self, flag):
        self.moving_down = flag
    def rotate_right_flag(self, flag):
        self.rotate_right = flag
    def rotate_left_flag(self, flag):
        self.rotate_left = flag
    def shooting_flag(self, flag):
        self.shooting = flag

    def _update_shooting(self):
        if self.frames > 0:
            self.frames -= 1
        if not self.shooting or self.frames != 0:
            return
        self.add_bullet(self.player_id, self.world)
        self.frames = self.frames_per_bullet

    def _update_rotation_angle(self, rotary):
        if self.rotate_right:
            rotary.current_angle_step = -rotary.angle_speed
        elif self.rotate_left:
            rotary.current_angle_step = rotary.angle_speed
        else:
            rotary.current_angle_step = 0

    def _directional_movable(self, mov, dir):
        if self.moving_up and not self.moving_down:
            mov.direction[1] = dir.move_up_dir[1]
            mov.direction[0] = dir.move_up_dir[0]
        elif not self.moving_up and self.moving_down:
            mov.direction[1] = dir.direction[1]
            mov.direction[0] = dir.direction[0]
        else:
            if mov.xspeed == 0:
                mov.direction[0] = 0
            if mov.yspeed == 0:
                mov.direction[1] = 0
        
    def _const_direction(self, mov):
        if self.moving_right and not self.moving_left:
            mov.direction[0] = 1
        elif not self.moving_right and self.moving_left:
            mov.direction[0] = -1
        elif mov.xspeed == 0:
            mov.direction[0] = 0

        if self.moving_up and not self.moving_down:
            mov.direction[1] = -1
        elif not self.moving_up and self.moving_down:
            mov.direction[1] = 1
        elif mov.yspeed == 0:
             mov.direction[1] = 0

    def _accelerating_directional_movement(self, acc):
        if self.moving_up or self.moving_down:
            acc.xacceleration = acc.base_acceleration
            acc.yacceleration = acc.base_acceleration
        else:
            acc.xacceleration = 0
            acc.yacceleration = 0

    def _accelerating_movement(self, acc):
        if self.moving_right or self.moving_left:
            acc.xacceleration = acc.base_acceleration
        else:
            acc.xacceleration = 0
        if self.moving_up or self.moving_down:
            acc.yacceleration = acc.base_acceleration
        else:
            acc.yacceleration = 0

    def _movement(self, mov):
        if self.moving_right or self.moving_left:
            mov.xspeed = mov.base_speed
        else:
            mov.xspeed = 0
        if self.moving_up or self.moving_down:
            mov.yspeed = mov.base_speed
        else:
            mov.yspeed = 0

    def process(self):
        if not self.world.entity_exists(self.player_id):
            return

        mov = self.world.try_component(self.player_id, movable)
        dir = self.world.try_component(self.player_id, directional)
        rot = self.world.try_component(self.player_id, rotary)
        acc = self.world.try_component(self.player_id, accelerating)

        if rot:
            self._update_rotation_angle(rot)
        if dir:
            self._directional_movable(mov, dir)
        else:
            self._const_direction(mov)
        if acc:
            if dir:
                self._accelerating_directional_movement(acc)
            else:
                self._accelerating_movement(acc)
        else:
            self._movement(mov)

        self._update_shooting()