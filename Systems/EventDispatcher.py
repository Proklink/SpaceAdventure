from ecs.ECS import Processor
from ecs.ECS import dispatch_event
from Components.rigid_body import rigid_body
import pygame, sys


class EventDispatcher(Processor):
    def __init__(self):
        super().__init__()


    def check_events_game_active(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    dispatch_event("moving_right", True)
                if event.key == pygame.K_a:
                    dispatch_event("moving_left", True)
                if event.key == pygame.K_w:
                    dispatch_event("moving_up", True)
                if event.key == pygame.K_s:
                    dispatch_event("moving_down", True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    dispatch_event("moving_right", False)
                if event.key == pygame.K_a:
                    dispatch_event("moving_left", False)
                if event.key == pygame.K_w:
                    dispatch_event("moving_up", False)
                if event.key == pygame.K_s:
                    dispatch_event("moving_down", False)

    def process(self):
        self.check_events_game_active()