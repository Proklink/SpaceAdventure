from ecs.ECS import Processor
from Components.movable import accelerating
from Components.movable import movable


class Accelerate(Processor):
    def __init__(self):
        super().__init__()

    def is_speed_max(self, mov, acc):
        if mov.speed > acc.max_speed:
            mov.speed = acc.max_speed
            return True
        return False

    def _update_speed(self, mov, acc):
        if (mov.direction[0] != 0 or mov.direction[1] != 0):
            if not self.is_speed_max(mov, acc):
                mov.speed += acc.acceleration

        elif mov.speed:
            if mov.speed >= -acc.acceleration and mov.speed <= acc.acceleration:
                mov.speed = 0
            else:
                mov.speed -= acc.acceleration

    def process(self):
        for ent, (mov, acc) in self.world.get_components(movable, accelerating):
            self._update_speed(mov, acc)