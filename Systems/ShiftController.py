from Components.movable import movable, accelerating
from ecs.ECS import Processor


class ShiftController(Processor):
    def __init__(self):
        super().__init__()

    def _process_speed(self, mov):
        mov.xshift = 0
        mov.yshift = 0
        if mov.xspeed != 0:
            mov.xshift = mov.xspeed * mov.direction[0]
        if mov.yspeed != 0:
            mov.yshift = mov.yspeed * mov.direction[1]
    
    def _process_speed_realistic(self, mov):
        mov.xshift = 0
        mov.yshift = 0
        if mov.xspeed != 0:
            mov.xshift = mov.xspeed
        if mov.yspeed != 0:
            mov.yshift = mov.yspeed

    def process(self):
        for ent, (mov) in self.world.get_component(movable):
            self._process_speed(mov)