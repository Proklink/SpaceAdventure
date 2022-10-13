from ecs.ECS import Processor
from Components.renderable import renderable
from screen import Screen
import pygame

class RenderProcessor(Processor):
    def __init__(self, window: Screen, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        self.window.screen.fill(self.clear_color)
        self.window.screen.blit(self.window.image, self.window.rect)

        for ent, rend in self.world.get_component(renderable):
            self.window.blit(rend.image, rend.rect)

        pygame.display.flip()