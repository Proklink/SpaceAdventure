import pygame
from ecs.ECS import set_handler
from ecs.ECS import dispatch_event
from screen import Screen
from settings import settings
from Systems.Game import Game
from Systems.Menu import Menu
import pygame, sys, threading

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
        dispatch_event("scripts_asyncs", False)
        self._menu.run()

    def game(self):
        dispatch_event("scripts_asyncs", True)
        self._game.run()

    def exit(self):
        dispatch_event("scripts_asyncs", False)
        cur_th = threading.current_thread()
        for th in threading.enumerate():
            if cur_th != th:
                th.join()
        pygame.quit()
        sys.exit()
