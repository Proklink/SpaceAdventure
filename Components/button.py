from dataclasses import dataclass as component
from Components.renderable import renderable
from settings import settings
import pygame

@component
class button:
    def __init__(self, msg, posx, posy):
        self.image = settings.but_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.but_font = pygame.font.SysFont(None, 48)

        # The button message needs to be prepped only once.
        self.msg_image = self.but_font.render(msg, True, settings.but_text_color, settings.but_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
        # self.image.blit(self.msg_image, self.msg_image_rect)

    def get_rend(self):
        return renderable(self.image.copy(), self.rect.centerx, self.rect.centery)

    def get_msg(self):
        return renderable(self.msg_image.copy(), self.msg_image_rect.centerx, self.msg_image_rect.centery)