from pygame.sprite import Sprite
from pygame.transform import rotate
from pygame.transform import smoothscale
import pygame
from pygame.color import THECOLORS


class Asteroid(Sprite):
    
    def __init__(self, xpos, ypos, screen, max_health, health_height, health_bar_shift, speed, damage, image):

        super(Asteroid, self).__init__()

        self.screen = screen

        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.image = smoothscale(self.image, (self.rect.width / 6, self.rect.height / 6))
        self.image = rotate(self.image, 180)
        self.rect = self.image.get_rect()

        self.rect.centerx = xpos
        self.rect.centery = ypos

        self.health = max_health
        self.max_health = max_health
        self.health_height = health_height
        self.health_bar_shift = health_bar_shift

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.direction = (0, 1)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.centerx += self.speed * self.direction[0]
        self.centery += self.speed * self.direction[1]
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def draw_health_bar(self):
        if self.health < 0:
            self.health = 0
        
        fill = (self.health / self.max_health) * self.rect.width

        outline_rect = pygame.Rect(self.rect.left, self.rect.top + 5, self.rect.width, self.health_height)
        fill_rect = pygame.Rect(self.rect.left, self.rect.top + 5, fill, self.health_height)

        pygame.draw.rect(self.screen, THECOLORS['red'], fill_rect)
        pygame.draw.rect(self.screen, THECOLORS['white'], outline_rect, 1)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.draw_health_bar()