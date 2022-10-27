import pygame
from pygame.transform import rotate

class left_right_moving():
    
    def __init__(self, entity, init_posx, init_posy, speed):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.speed = speed

        self.entity = entity

        self.init_posx = init_posx
        self.init_posy = init_posy

        self.entity.rect.centerx = init_posx
        self.entity.rect.centery = init_posy

        self.centerx = float(self.entity.rect.centerx)
        self.centery = float(self.entity.rect.centery)

    def get_current_direction(self):
        return [0, 1]

    def reset_pos(self):
        self.entity.rect.centerx = self.entity.collideRect.centerx = self.init_posx
        self.entity.rect.centery = self.entity.collideRect.centery = self.init_posy

    def on_switch(self):
        self.centerx = float(self.entity.rect.centerx)
        self.centery = float(self.entity.rect.centery)

        self.entity.image = rotate(self.entity.original, 0)
        self.entity.rect = self.entity.image.get_rect(center=self.entity.rect.center)

    def get_move_left_right_shift(self):
        if self.moving_right:
            return self.speed
        if self.moving_left:
            return -self.speed

    def get_move_up_down_shift(self):
        if self.moving_up:
            return -self.speed
        if self.moving_down:
            return self.speed

    def update_position(self, access_to_move_x, access_to_move_y):
        if access_to_move_y and (self.moving_up or self.moving_down):
            self.centery += self.get_move_up_down_shift()
            self.entity.rect.centery = self.centery
            self.entity.collideRect.centery = self.entity.rect.centery
        if access_to_move_x and (self.moving_right or self.moving_left):
            self.centerx += self.get_move_left_right_shift()
            self.entity.rect.centerx = self.centerx
            self.entity.collideRect.centerx = self.entity.rect.centerx

    def update_collision_with_map(self):
        # SRiNF = self's rect in next frame

        SRiNF = self.entity.collideRect.copy()
        if self.moving_up or self.moving_down:
            SRiNF.centery += self.get_move_up_down_shift()
        if self.moving_right or self.moving_left:
            SRiNF.centerx += self.get_move_left_right_shift()

        access_to_move_x = True
        access_to_move_y = True

        if SRiNF.bottom >= self.entity.screen.height or \
           SRiNF.top <= 0:
            access_to_move_y = False
        if SRiNF.left <= 0 or \
           SRiNF.right >= self.entity.screen.width:
            access_to_move_x = False

        return access_to_move_x, access_to_move_y

    def update(self):
        access_to_move_x, access_to_move_y = self.update_collision_with_map()
        self.update_position(access_to_move_x, access_to_move_y)

    def check_moving_events_keydown(self, event):
        if event.key == pygame.K_d:
            self.moving_right = True
        if event.key == pygame.K_a:
            self.moving_left = True
        if event.key == pygame.K_w:
            self.moving_up = True
        if event.key == pygame.K_s:
            self.moving_down = True
    
    def check_moving_events_keyup(self, event):
        if event.key == pygame.K_d:
            self.moving_right = False
        if event.key == pygame.K_a:
            self.moving_left = False
        if event.key == pygame.K_w:
            self.moving_up = False
        if event.key == pygame.K_s:
            self.moving_down = False
