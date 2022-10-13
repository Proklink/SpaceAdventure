from Components.movable import movable
from ecs.ECS import Processor
from Components.movable import movable


class ShiftController(Processor):
    def __init__(self, id):
        super().__init__()

    def _process_speed(self, mov):
        if mov.direction[0] > 0:
            mov.xshift = mov.speed
        if mov.direction[0] < 0:
            mov.xshift = -mov.speed
        if mov.direction[1] < 0:
            mov.yshift = -mov.speed
        if mov.direction[1] > 0:
            mov.yshift = mov.speed

    def process(self):
        for ent, (mov) in self.world.get_components(movable):
            self._process_speed(mov)