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
    
    def speed_max(self, speed, max_speed):
        if abs(speed) > max_speed:
            if speed > 0:
                speed = max_speed
            else:
                speed = -max_speed

        return speed

    def _decrease_speed(self, speed, acc):
        if speed >= -acc.base_acceleration and speed <= acc.base_acceleration:
            speed = 0
        elif speed > 0:
            speed -= acc.base_acceleration
        elif speed < 0:
            speed += acc.base_acceleration
        return speed

    def _update_speed_realistic(self, mov, acc):
        if (acc.xacceleration):
            mov.xspeed += acc.xacceleration * mov.direction.x
            mov.xspeed = self.speed_max(mov.xspeed, acc.max_speed)
        else:
            if mov.xspeed:
                mov.xspeed = self._decrease_speed(mov.xspeed, acc)
        if (acc.yacceleration):
            mov.yspeed += acc.yacceleration * mov.direction.y
            mov.yspeed = self.speed_max(mov.yspeed, acc.max_speed)
        else:
            if mov.yspeed:
                mov.yspeed = self._decrease_speed(mov.yspeed, acc)

    def _update_speed(self, speed, acceleration, acc):
        if (acceleration):
            speed += acceleration
            speed = self.speed_max(speed, acc.max_speed)
        else:
            if speed:
                speed = self._decrease_speed(speed, acc)
        return speed

    def process(self):
        for ent, (mov, acc) in self.world.get_components(movable, accelerating):
            # self._update_speed_realistic(mov, acc)
            mov.xspeed = self._update_speed(mov.xspeed, acc.xacceleration, acc)
            mov.yspeed = self._update_speed(mov.yspeed, acc.yacceleration, acc)