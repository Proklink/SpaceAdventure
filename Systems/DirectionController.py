from ecs.ECS import Processor
from Components.movable import rotary, directional
import math

class DirectionController(Processor):
    def __init__(self):
        super().__init__()

    def _update_direction(self, rot, direct):
        direct.direction[0] = math.sin(math.radians(rot.current_angle))
        direct.direction[1] = math.cos(math.radians(rot.current_angle))
        direct.move_up_dir[0] = -1 * direct.direction[0]
        direct.move_up_dir[1] = -1 * direct.direction[1]

    def process(self):
        for ent, (rot, direct) in self.world.get_components(rotary, directional):
            self._update_direction(rot, direct)