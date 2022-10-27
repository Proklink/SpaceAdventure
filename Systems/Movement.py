from ecs.ECS import Processor
from Components.movable import movable
from Components.renderable import renderable
from Components.rigid_body import rigid_body


class Movement(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def reset_pos(self, rend, rb):
        rend.rect.centerx = rb.collide_rect.centerx = rend.init_posx
        rend.rect.centery = rb.collide_rect.centery = rend.init_posy

    def update_position(self, access_to_move_x, access_to_move_y, mov, rend, rb):
        if access_to_move_y and mov.yshift:
            rend.centery += mov.yshift
            rend.rect.centery = rend.centery
            rb.collide_rect.centery = rend.centery

        if access_to_move_x and mov.xshift:
            rend.centerx += mov.xshift
            rend.rect.centerx = rend.centerx
            rb.collide_rect.centerx = rend.centerx

    def update_collision_with_map(self, CRiNF, mov):
        # CRiNF = collide rect in next frame

        if mov.yshift != 0:
            CRiNF.centery += mov.yshift
        if mov.xshift != 0:
            CRiNF.centerx += mov.xshift

        access_to_move_x = True
        access_to_move_y = True

        if CRiNF.bottom >= self.maxy or CRiNF.top <= self.miny:
            access_to_move_y = False
        if CRiNF.left <= self.minx or CRiNF.right >= self.maxx:
            access_to_move_x = False

        return access_to_move_x, access_to_move_y

    def process(self):
        #возможно, коллизии с картой лучше вынести в другое место
        for ent, (mov, rend, rb) in self.world.get_components(movable, renderable, rigid_body):
            move_x, move_y = self.update_collision_with_map(rb.collide_rect.copy(), mov)
            self.update_position(move_x, move_y, mov, rend, rb)
