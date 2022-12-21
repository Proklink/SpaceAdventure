import pygame
from ecs.ECS import set_handler
from screen import Screen
from settings import settings
from Systems.Game import Game
from Systems.Menu import Menu
import pygame, sys

class GameController:
    def __init__(self):
        pygame.init()

        self.screen = Screen(settings.scr_width,
                             settings.scr_height,
                             settings.scr_caption,
                             settings.scr_image)
        self._game = Game(self.screen)
        self._menu = Menu(self.screen)

        set_handler("menu", self.menu)
        set_handler("game", self.game)
        set_handler("exit", self.exit)
        self.menu()


    def menu(self):
        self._menu.run()

    def game(self):
        self._game.run()

    def exit(self):
        pygame.quit()
        sys.exit()
