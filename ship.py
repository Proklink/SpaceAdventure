from pygame.transform import smoothscale

from pygame.sprite import Sprite
from pygame.color import THECOLORS
import pygame

class Ship(Sprite):

    def __init__(self, screen, image, max_health, health_height,
                 health_bar_shift, lives_limit, damage):
        """Initialize the ship and set its starting position."""
        
        super(Ship, self).__init__()

        self.screen = screen
        
        # Load the ship image and get its rect.
        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.image = smoothscale(self.image, (self.rect.width / 4, self.rect.height / 4))
        self.rect = self.image.get_rect()
        self.original = self.image.copy()

        self.shooting = False
        self.moving_component = None

        self.health = max_health
        self.max_health = max_health
        self.health_height = health_height
        self.health_bar_shift = health_bar_shift

        self.lives_limit = lives_limit
        self.damage = damage

        self.frames_per_bullet = 20
        self.frames = 0

    def draw_health_bar(self):
        if self.health < 0:
            self.health = 0
        
        fill = (self.health / self.max_health) * self.collideRect.width

        outline_rect = pygame.Rect(self.collideRect.left, self.collideRect.top - self.health_bar_shift, self.collideRect.width, self.health_height)
        fill_rect = pygame.Rect(self.collideRect.left, self.collideRect.top - self.health_bar_shift, fill, self.health_height)

        pygame.draw.rect(self.screen.screen, THECOLORS['red'], fill_rect)
        pygame.draw.rect(self.screen.screen, THECOLORS['white'], outline_rect, 1)
        
    def set_moving(self, moving):
        self.moving_component = moving
        self.collideRect = self.rect.copy()
        self.moving_component.on_switch()

    def get_current_direction(self):
        if self.moving_component != None:
            return self.moving_component.get_current_direction()
        else:
            return [0, 1]

    def reset_ship(self):
        self.moving_component.reset_pos()

    def update(self, bullets):
        """Update the ship's position based on the movement flag."""
        
        self.moving_component.update()

        if self.frames > 0:
            self.frames -= 1

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.screen.blit(self.image, self.rect)
        self.draw_health_bar()

    def check_moving_events_keydown(self, event):
        self.moving_component.check_moving_events_keydown(event)

    def check_moving_events_keyup(self, event):
        self.moving_component.check_moving_events_keyup(event)
        