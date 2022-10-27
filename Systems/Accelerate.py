from ecs.ECS import Processor
from Components.movable import accelerating
from Components.movable import movable

class Accelerate(Processor):
    def __init__(self):
        super().__init__()

    def is_speed_max(self, speed, acc):
        if abs(speed) > acc.max_speed:
            if speed > 0:
                speed = acc.max_speed
            else:
                speed = -acc.max_speed
            return True
        return False

    def _decrease_speed(self, speed, acc):
        if speed >= -acc.base_acceleration and speed <= acc.base_acceleration:
            speed = 0
        elif speed > 0:
            speed -= acc.base_acceleration
        elif speed < 0:
            speed += acc.base_acceleration
        return speed

    def _update_speed(self, mov, acc):
        if (acc.acceleration):
            if not self.is_speed_max(mov.xspeed, acc):
                mov.xspeed += acc.acceleration
            if not self.is_speed_max(mov.yspeed, acc):
                mov.yspeed += acc.acceleration
        else:
            if mov.xspeed:
                mov.xspeed = self._decrease_speed(mov.xspeed, acc)
            if mov.yspeed:
                mov.yspeed = self._decrease_speed(mov.yspeed, acc)

    def process(self):
        for ent, (mov, acc) in self.world.get_components(movable, accelerating):
            self._update_speed(mov, acc)