import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, screen, direction, width, height, color, speed, damage, image, xpos, ypos):
        """Create a bullet object at the ship's current position."""
        
        super(Bullet, self).__init__()

        self.screen = screen
        self.bullet_width = width
        self.bullet_height = height
        self.color = color
        self.speed = speed
        self.damage = damage

        self.image = image.copy().convert_alpha()
        pygame.draw.ellipse(self.bul_image, self.bul_color, (0, 0, self.bul_width, self.bul_height))

        self.direction = direction

        self.rect = self.image.get_rect()

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect.centerx = xpos
        self.rect.centery = ypos

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""

        self.y += self.speed * -self.direction[1]
        self.x += self.speed * -self.direction[0]

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the alien at its current location."""

        self.screen.blit(self.image, self.rect)