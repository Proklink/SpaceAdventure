from ecs.ECS import Processor
from ecs.ECS import dispatch_event
import pygame, sys
from Components.movable import directional 


class EventDispatcher(Processor):
    def __init__(self, id):
        super().__init__()

        self.player_id = id


    def check_events_game_active(self, dir):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if dir:
                        dispatch_event("rotate_right", True)
                    else:
                        dispatch_event("moving_right", True)
                if event.key == pygame.K_a:
                    if dir:
                        dispatch_event("rotate_left", True)
                    else:
                        dispatch_event("moving_left", True)
                if event.key == pygame.K_w:
                    dispatch_event("moving_up", True)
                if event.key == pygame.K_s:
                    dispatch_event("moving_down", True)
                #чтобы не пересекались с K_d и K_a
                if not dir:
                    if event.key == pygame.K_RIGHT:
                        dispatch_event("rotate_right", True)
                    if event.key == pygame.K_LEFT:
                        dispatch_event("rotate_left", True)
                if event.key == pygame.K_SPACE:
                    dispatch_event("shooting", True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    if dir:
                        dispatch_event("rotate_right", False)
                    else:
                        dispatch_event("moving_right", False)
                if event.key == pygame.K_a:
                    if dir:
                        dispatch_event("rotate_left", False)
                    else:
                        dispatch_event("moving_left", False)
                if event.key == pygame.K_w:
                    dispatch_event("moving_up", False)
                if event.key == pygame.K_s:
                    dispatch_event("moving_down", False)
                #чтобы не пересекались с K_d и K_a
                if not dir:
                    if event.key == pygame.K_RIGHT:
                        dispatch_event("rotate_right", False)
                    if event.key == pygame.K_LEFT:
                        dispatch_event("rotate_left", False)
                if event.key == pygame.K_SPACE:
                    dispatch_event("shooting", False)

    def process(self):
        dir = None
        if self.world.entity_exists(self.player_id):
            dir = self.world.try_component(self.player_id, directional)
        self.check_events_game_active(dir)