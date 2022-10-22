from ecs.ECS import Processor
from Components.controllable import controllable
from Components.movable import movable, rotary, directional 

class PlayerController(Processor):
    def __init__(self, id):
        super().__init__()
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.rotate_right = False
        self.rotate_left = False
        self.player_id = id

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

    def _update_rotation_angle(self, rotary):
        if self.rotate_right:
            rotary.current_angle_step = -rotary.angle_speed
        elif self.rotate_left:
            rotary.current_angle_step = rotary.angle_speed
        else:
            rotary.current_angle_step = 0

    def _process_directional_movable(self, mov, dir):
        mov.direction = dir.current_direction
           
        if self.moving_up and not self.moving_down:
            mov.direction[1] *= -1
            mov.direction[0] *= -1
        elif not self.moving_up and self.moving_down:
            mov.direction[1] *= 1
            mov.direction[0] *= 1
        else:
            mov.direction[0] = 0
            mov.direction[1] = 0
        
    def _process_movable(self, mov):
        xdir = 0
        ydir = 0
        if self.moving_right and not self.moving_left:
            xdir = 1
        elif not self.moving_right and self.moving_left:
            xdir = -1
        if self.moving_up and not self.moving_down:
            ydir = -1
        elif not self.moving_up and self.moving_down:
            ydir = 1

        mov.direction = [xdir, ydir]

    def process(self):
        if not self.world.entity_exists(self.player_id):
            return

        mov = self.world.try_component(self.player_id, movable)
        dir = self.world.try_component(self.player_id, directional)
        rot = self.world.try_component(self.player_id, rotary)

        if rot:
            self._update_rotation_angle(rot)
        if dir:
            self._process_directional_movable(mov, dir)
        else:
            self._process_movable(mov)