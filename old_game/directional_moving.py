import math
from pygame.transform import rotate
import pygame

class directional_moving():
    def __init__(self, entity, init_posx, init_posy, acceleration, max_speed, angle_speed, init_direction):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.rotate_right = False
        self.rotate_left = False

        self.entity = entity

        self.acceleration = acceleration
        self.speed = 0
        self.max_speed = max_speed
        self.angle_speed = angle_speed
        self.current_direction = init_direction
        self.current_angle = 0

        self.init_posx = init_posx
        self.init_posy = init_posy

        self.entity.rect.centerx = init_posx
        self.entity.rect.centery = init_posy

        self.centerx = float(self.entity.rect.centerx)
        self.centery = float(self.entity.rect.centery)

    def get_current_direction(self):
        return self.current_direction.copy()

    def reset_pos(self):
        self.entity.rect.centerx = self.entity.collideRect.centerx = self.init_posx
        self.entity.rect.centery = self.entity.collideRect.centery = self.init_posy

    def on_switch(self):
        self.centerx = float(self.entity.rect.centerx)
        self.centery = float(self.entity.rect.centery)
        self.current_direction = self.entity.get_current_direction()

    def update_direction(self):
        self.current_direction[0] = math.sin(math.radians(self.current_angle))
        self.current_direction[1] = math.cos(math.radians(self.current_angle))

    def is_speed_max(self):
        if self.speed > self.max_speed:
            self.speed = self.max_speed
            return True
        elif self.speed < -self.max_speed:
            self.speed = -self.max_speed
            return True
        return False

    def update_rotation(self):
        if self.rotate_right or self.rotate_left:
            if self.rotate_right:
                self.current_angle = (self.current_angle - self.angle_speed) % 360
            if self.rotate_left:
                self.current_angle = (self.current_angle + self.angle_speed) % 360

            self.entity.image = rotate(self.entity.original, self.current_angle)
            self.entity.rect = self.entity.image.get_rect(center=self.entity.rect.center)

    def update_speed(self):
        if (self.moving_up or self.moving_down) and not self.is_speed_max():
            if self.moving_up:
                self.speed -= self.acceleration
                
            if self.moving_down:
                self.speed += self.acceleration
        elif self.speed:
            if self.speed >= -self.acceleration and self.speed <= self.acceleration:
                self.speed = 0
            elif self.speed > 0:
                self.speed -= self.acceleration
            elif self.speed < 0:
                self.speed += self.acceleration

    def update_position(self, access_to_move_x, access_to_move_y):
        if self.speed:
            if access_to_move_y:
                self.centery += self.speed * self.current_direction[1]
                self.entity.rect.centery = self.centery
                self.entity.collideRect.centery = self.entity.rect.centery
            if access_to_move_x:
                self.centerx += self.speed * self.current_direction[0]
                self.entity.rect.centerx = self.centerx
                self.entity.collideRect.centerx = self.entity.rect.centerx

    def update_collision_with_map(self):
        # SRiNF = self's rect in next frame

        SRiNF = self.entity.collideRect.copy()
        if self.speed != 0:
            SRiNF.centery += self.speed * self.current_direction[1]
            SRiNF.centerx += self.speed * self.current_direction[0]

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
        self.update_rotation()
        self.update_direction()
        self.update_speed()
        access_to_move_x, access_to_move_y = self.update_collision_with_map()
        self.update_position(access_to_move_x, access_to_move_y)

    def check_moving_events_keydown(self, event):
        if event.key == pygame.K_w:
            self.moving_up = True
        if event.key == pygame.K_s:
            self.moving_down = True

        if event.key == pygame.K_d:
            self.rotate_right = True
        if event.key == pygame.K_a:
            self.rotate_left = True
    
    def check_moving_events_keyup(self, event):
        if event.key == pygame.K_w:
            self.moving_up = False
        if event.key == pygame.K_s:
            self.moving_down = False

        if event.key == pygame.K_d:
            self.rotate_right = False
        if event.key == pygame.K_a:
            self.rotate_left = False
