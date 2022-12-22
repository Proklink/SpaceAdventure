from ecs.ECS import Processor
from Components.movable import movable
from Components.renderable import renderable
from Components.rigid_body import rigid_body


class PlayerMapCollision(Processor):
    def __init__(self, minx, maxx, miny, maxy, id):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.player_id = id

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
        if not self.world.entity_exists(self.player_id):
            return

        mov = self.world.try_component(self.player_id, movable)
        rb = self.world.try_component(self.player_id, rigid_body)
        if not mov and not rb:
            return
        move_x, move_y = self.update_collision_with_map(rb.collide_rect.copy(), mov)
        if not move_x:
            mov.xshift = 0
        if not move_y:
            mov.yshift = 0
