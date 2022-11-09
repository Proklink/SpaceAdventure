from ecs.ECS import Processor
from Components.movable import movable
from Components.renderable import renderable
from Components.rigid_body import rigid_body


class Movement(Processor):
    def __init__(self):
        super().__init__()

    def reset_pos(self, rend, rb):
        rend.rect.centerx = rb.collide_rect.centerx = rend.init_posx
        rend.rect.centery = rb.collide_rect.centery = rend.init_posy

    def update_position(self, mov, rend, rb):
        if mov.yshift:
            rend.centery += mov.yshift
            rend.rect.centery = rend.centery
            rb.collide_rect.centery = rend.centery

        if mov.xshift:
            rend.centerx += mov.xshift
            rend.rect.centerx = rend.centerx
            rb.collide_rect.centerx = rend.centerx

    def process(self):
        for ent, (mov, rend, rb) in self.world.get_components(movable, renderable, rigid_body):
            self.update_position(mov, rend, rb)
