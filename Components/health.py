from dataclasses import dataclass as component
from pygame.color import THECOLORS
import pygame

@component
class destructible:
    def __init__(self, health, max_health, lives_limit):
        self.health = health
        self.max_health = max_health
        self.lives_limit = lives_limit

@component
class health_bar:
    def __init__(self, shift_from_object, health_bar_height, rb_top, rb_left, rb_width):
        self.shift_from_object = shift_from_object
        self.height = health_bar_height
        self.fill_color = THECOLORS['red']
        self.outline_color = THECOLORS['white']

        self.outline_rect = pygame.Rect(rb_left, rb_top - shift_from_object, rb_width, health_bar_height)
        self.fill_rect = pygame.Rect(rb_left, rb_top - shift_from_object, rb_width, health_bar_height)
        self.outline_surf = pygame.Surface((self.outline_rect.width, self.outline_rect.top))
        self.outline_surf.fill(self.outline_color)
        self.fill_surf = pygame.Surface((self.fill_rect.width, self.fill_rect.top))
        self.fill_surf.fill(self.fill_color)


@component
class damage:
    def __init__(self, damage):
        self.damage = damage