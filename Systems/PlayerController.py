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
        else:
            rotary.current_angle_step = 0
        if self.rotate_left:
            rotary.current_angle_step = rotary.angle_speed
        else:
            rotary.current_angle_step = 0
        
    def _process_movable(self, dir, mov):
        if dir:
            mov.direction = dir.current_direction
        else:
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
        if not self.world.entity_exists(self.player_id): #or not self.world.has_component(self.player_id, controllable):
            return
        #так же какой компонент будет при этом использовать флаги перемещения и когда какие кнопки
        #отвечают за движение по x, а какие за повороты
        mov = self.world.component_for_entity(self.player_id, movable)
        dir = self.world.component_for_entity(self.player_id, directional)
        rot = self.world.component_for_entity(self.player_id, rotary)

        if rot:
            self._update_rotation_angle(rot)
        if mov:
            self._process_movable(dir, mov)