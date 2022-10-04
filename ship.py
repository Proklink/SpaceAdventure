from pygame.image import load
from pygame.transform import smoothscale
from pygame.transform import rotate
from pygame.sprite import Sprite
import math
from pygame.color import THECOLORS
import pygame
import bullet

class Ship(Sprite):

    def __init__(self, screen, acceleration, max_speed, angle_speed, init_direction,
                 image, max_health, health_height, health_bar_shift, lives_limit,
                 damage, init_posx, init_posy):
        """Initialize the ship and set its starting position."""
        
        super(Ship, self).__init__()

        self.screen = screen

        self.acceleration = acceleration
        self.speed = 0
        self.max_speed = max_speed
        self.angle_speed = angle_speed
        self.current_direction = init_direction
        self.current_angle = 0
        
        # Load the ship image and get its rect.
        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.image = smoothscale(self.image, (self.rect.width / 4, self.rect.height / 4))
        self.rect = self.image.get_rect()

        self.original = self.image.copy()

        self.init_posx = init_posx
        self.init_posy = init_posy

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = init_posx
        self.rect.bottom = init_posx

        self.collideRect = self.rect.copy()

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.shooting = False

        self.rotate_right = False
        self.rotate_left = False

        self.health = max_health
        self.max_health = max_health
        self.health_height = health_height
        self.health_bar_shift = health_bar_shift

        self.score = 0

        self.lives_limit = lives_limit
        self.damage = damage

    def init_pos_ship(self):
        """Center the ship on the screen."""

        self.center = self.init_posx
        self.rect.bottom = self.init_posy

    def draw_health_bar(self):
        if self.health < 0:
            self.health = 0
        
        fill = (self.health / self.max_health) * self.collideRect.width

        outline_rect = pygame.Rect(self.collideRect.left, self.collideRect.top - self.health_bar_shift, self.collideRect.width, self.health_height)
        fill_rect = pygame.Rect(self.collideRect.left, self.collideRect.top - self.health_bar_shift, fill, self.health_height)

        pygame.draw.rect(self.screen.screen, THECOLORS['red'], fill_rect)
        pygame.draw.rect(self.screen.screen, THECOLORS['white'], outline_rect, 1)
        
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

            self.image = rotate(self.original, self.current_angle)
            self.rect = self.image.get_rect(center=self.rect.center)

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
            
    def update_collision_with_map(self):
        # SRiNF = ship's rect in next frame

        SRiNF = self.collideRect.copy()
        if self.speed != 0:
            SRiNF.centery += self.speed * self.current_direction[1]
            SRiNF.centerx += self.speed * self.current_direction[0]

        access_to_move_x = True
        access_to_move_y = True

        if SRiNF.bottom >= self.screen.height or \
           SRiNF.top <= 0:
            access_to_move_y = False
        if SRiNF.left <= 0 or \
           SRiNF.right >= self.screen.width:
            access_to_move_x = False

        return access_to_move_x, access_to_move_y

    def update_position(self, access_to_move_x, access_to_move_y):
        if self.speed:
            if access_to_move_y:
                self.centery += self.speed * self.current_direction[1]
                self.rect.centery = self.centery
                self.collideRect.centery = self.rect.centery
            if access_to_move_x:
                self.centerx += self.speed * self.current_direction[0]
                self.rect.centerx = self.centerx
                self.collideRect.centerx = self.rect.centerx

    def update(self, bullets):
        """Update the ship's position based on the movement flag."""
        
        self.update_rotation()
        self.update_direction()
        self.update_speed()
        access_to_move_x, access_to_move_y = self.update_collision_with_map()
        self.update_position(access_to_move_x, access_to_move_y)

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.screen.blit(self.image, self.rect)
        self.draw_health_bar()
        