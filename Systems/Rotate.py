from ecs.ECS import Processor
from Components.movable import rotary
from Components.movable import movable
from Components.renderable import renderable
from pygame.transform import rotate



class Rotate(Processor):
    def __init__(self):
        super().__init__()

    def _update_rotation(self, rot, rend):
        if rot.current_angle_step:
            rot.current_angle = (rot.current_angle + rot.current_angle_step) % 360

            rend.image = rotate(rot.original_image, rot.current_angle)
            rend.rect = rend.image.get_rect(center=rend.rect.center)

    def process(self):
        for ent, (rot, rend) in self.world.get_components(rotary, renderable):
            self._update_rotation(rot, rend)