from ecs.ECS import Processor
from Components.movable import rotary, directional
import math

class DirectionController(Processor):
    def __init__(self):
        super().__init__()

    def _update_direction(self, rot, direct):
        direct.current_direction[0] = math.sin(math.radians(rot.current_angle))
        direct.current_direction[1] = math.cos(math.radians(rot.current_angle))

    def process(self):
        for ent, (rot, direct) in self.world.get_components(rotary, directional):
            self._update_direction(rot, direct)