from ecs.ECS import Processor
from Components.movable import movable
from Components.renderable import renderable
from Components.rigid_body import rigit_body


class Movement(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def get_current_direction(self):
        return [0, 1]

    def reset_pos(self, rend, rb):
        rend.rect.centerx = rb.collide_rect.centerx = rend.init_posx
        rend.rect.centery = rb.collide_rect.centery = rend.init_posy

    def get_move_left_right_shift(self, mov):
        if mov.moving_right:
            return mov.speed
        if mov.moving_left:
            return -mov.speed

    def get_move_up_down_shift(self, mov):
        if mov.moving_up:
            return -mov.speed
        if mov.moving_down:
            return mov.speed

    def update_position(self, access_to_move_x, access_to_move_y, mov, rend, rb):
        if access_to_move_y and (mov.moving_up or mov.moving_down):
            rend.centery += self.get_move_up_down_shift()
            rend.rect.centery = rend.centery
            rb.collide_rect.centery = rend.centery

        if access_to_move_x and (mov.moving_right or mov.moving_left):
            rend.centerx += self.get_move_left_right_shift()
            rend.rect.centerx = rend.centerx
            rb.collide_rect.centerx = rend.centerx

    def update_collision_with_map(self, SRiNF, xshift, yshift):
        # SRiNF = self's rect in next frame

        if self.moving_up or self.moving_down:
            SRiNF.centery += yshift
        if self.moving_right or self.moving_left:
            SRiNF.centerx += xshift

        access_to_move_x = True
        access_to_move_y = True

        if SRiNF.bottom >= self.maxy or SRiNF.top <= self.miny:
            access_to_move_y = False
        if SRiNF.left <= self.minx or SRiNF.right >= self.maxx:
            access_to_move_x = False

        return access_to_move_x, access_to_move_y

    def process(self):
        for ent, (mov, rend, rb) in self.world.get_components(movable, renderable, rigit_body):
            xshift = self.get_move_left_right_shift(mov)
            yshift = self.get_move_up_down_shift(mov)
            move_x, move_y = self.update_collision_with_map(rb.collide_rect.copy(), xshift, yshift)
            self.update_position(move_x, move_y, mov, rend, rb)