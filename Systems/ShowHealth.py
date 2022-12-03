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

        left = rb.collide_rect.left
        top = rb.collide_rect.top - hl_bar.shift_from_object

        # hl_bar.outline_rect.left = rb.collide_rect.left
        # hl_bar.outline_rect.top = rb.collide_rect.top - hl_bar.shift_from_object
        # hl_bar.fill_rect.left = rb.collide_rect.left
        # hl_bar.fill_rect.top = rb.collide_rect.top - hl_bar.shift_from_object
        # hl_bar.fill_rect.width = fill
        # hl_bar.fill_surf = pygame.Surface((hl_bar.fill_rect.width, hl_bar.fill_rect.top))
        # hl_bar.fill_surf.fill(hl_bar.fill_color)

        # outline_rect = pygame.Rect(rb.collide_rect.left, rb.collide_rect.top - hl_bar.shift_from_object, rb.collide_rect.width, hl_bar.height)
        # fill_rect = pygame.Rect(rb.collide_rect.left, rb.collide_rect.top - hl_bar.shift_from_object, fill, hl_bar.height)
        # outline_rect = pygame.Rect(rb.collide_rect.left, rb.collide_rect.top - hl_bar.shift_from_object, rb.collide_rect.width, hl_bar.height)
        # fill_rect = pygame.Rect(rb.collide_rect.left, rb.collide_rect.top - hl_bar.shift_from_object, fill, hl_bar.height)

        # pygame.draw.rect(self.window.screen, THECOLORS['red'], fill_rect)
        # pygame.draw.rect(self.window.screen, THECOLORS['white'], outline_rect, 1)
        self.window.screen.blit(hl_bar.outline_surf, hl_bar.outline_rect)
        self.window.screen.blit(hl_bar.fill_surf, hl_bar.fill_rect)

    def process(self):
        for ent, (rb, dest, hl_bar) in self.world.get_components(rigid_body, destructible, health_bar):
            self.draw_health_bar(rb, dest, hl_bar)