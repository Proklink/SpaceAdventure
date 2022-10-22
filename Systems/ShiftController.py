from Components.movable import movable
from ecs.ECS import Processor
from Components.movable import movable


class ShiftController(Processor):
    def __init__(self):
        super().__init__()

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
        for ent, (mov) in self.world.get_component(movable):
            self._process_speed(mov)