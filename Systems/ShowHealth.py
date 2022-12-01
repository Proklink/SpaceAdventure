from pygame.color import THECOLORS
from ecs.ECS import Processor
from screen import Screen
from Components.rigid_body import rigid_body
from Components.health import destructible, health_bar
import pygame

class ShowHealth(Processor):
    def __init__(self, window: Screen):
        super().__init__()
        self.window = window

    def draw_health_bar(self, rb, dest, hl_bar):
        if dest.health < 0:
            dest.health = 0
        
        fill = (dest.health / dest.max_health) * rb.collide_rect.width

        outline_rect = pygame.Rect(rb.collide_rect.left, rb.collide_rect.top - hl_bar.shift_from_object, rb.collide_rect.width, hl_bar.height)
        fill_rect = pygame.Rect(rb.collide_rect.left, rb.collide_rect.top - hl_bar.shift_from_object, fill, hl_bar.height)

        pygame.draw.rect(self.window.image, THECOLORS['red'], fill_rect)
        pygame.draw.rect(self.window.image, THECOLORS['white'], outline_rect, 1)

    def process(self):
        for ent, (rb, dest, hl_bar) in self.world.get_components(rigid_body, destructible, health_bar):
            self.draw_health_bar(rb, dest, hl_bar)