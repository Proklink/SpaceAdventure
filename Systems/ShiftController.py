from Components.movable import movable, accelerating
from ecs.ECS import Processor


class ShiftController(Processor):
    def __init__(self):
        super().__init__()

    def _process_speed_with_acceleration(self, mov, acc):
        mov.xshift = 0
        mov.yshift = 0
        if mov.speed > 0:
            mov.xshift = mov.speed * mov.direction[0]
            mov.yshift = mov.speed * mov.direction[1]
           
    
    def _process_speed(self, mov):
        mov.xshift = 0
        mov.yshift = 0
        if mov.direction[0] > 0:
            mov.xshift = mov.speed * mov.direction[0]
        if mov.direction[0] < 0:
            mov.xshift = mov.speed * mov.direction[0]
        if mov.direction[1] < 0:
            mov.yshift = mov.speed * mov.direction[1]
        if mov.direction[1] > 0:
            mov.yshift = mov.speed * mov.direction[1]

    def process(self):
        for ent, (mov, acc) in self.world.get_components(movable, accelerating):
            if acc:
                self._process_speed_with_acceleration(mov, acc)
            else:
                self._process_speed(mov)