from ecs.ECS import Processor
from Components.movable import accelerating
from Components.movable import movable


class Accelerate(Processor):
    def __init__(self):
        super().__init__()

    def is_speed_max(self, mov, acc):
        if mov.speed > mov.max_speed:
            mov.speed = mov.max_speed
            return True
        elif mov.speed < -mov.max_speed:
            mov.speed = -mov.max_speed
            return True
        return False

    def _update_speed(self, mov, acc):
        if mov.speed > mov.max_speed:
            mov.speed = mov.max_speed
        else:
            mov.speed += acc.acceleration

    def process(self):
        for ent, (mov, acc) in self.world.get_components(movable, accelerating):
            self._update_speed(mov, acc)