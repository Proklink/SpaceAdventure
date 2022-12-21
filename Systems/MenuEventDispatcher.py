from ecs.ECS import Processor
from ecs.ECS import dispatch_event
import pygame, sys

from settings import settings


class MenuEventDispatcher(Processor):
    def __init__(self, play_button_rect, exit_button_rect):
        super().__init__()
        self.play_button_rect = play_button_rect
        self.exit_button_rect = exit_button_rect

    def check_menu_buttons(self, mouse_x, mouse_y):
        if self.play_button_rect.collidepoint(mouse_x, mouse_y):
            dispatch_event("game")
        if self.exit_button_rect.collidepoint(mouse_x, mouse_y):
            dispatch_event("exit")

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dispatch_event("exit")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_menu_buttons(mouse_x, mouse_y)

    def process(self):
        self.check_events()