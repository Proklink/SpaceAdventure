from Systems.MenuEventDispatcher import MenuEventDispatcher
from Systems.Render import Render
from ecs.ECS import World

from settings import settings
from ecs.ECS import set_handler
from Components.renderable import renderable
from Components.button import button

class Menu:
    def __init__(self, screen):
        self.world = World()
        
        self.play_button = button("Play", settings.scr_width / 2, settings.scr_height / 2)
        self.exit_button = button("Exit", settings.scr_width / 2, settings.scr_height / 2 + 2 * 50)
        # self.black_background = renderable(settings.mb_image.copy(), 0, 0)
        self.play_b = self.world.create_entity()
        self.exit_b = self.world.create_entity()
        self.play_b_msg = self.world.create_entity()
        self.exit_b_msg = self.world.create_entity()
        # self.menu_background = self.world.create_entity()

        self.world.add_component(self.play_b, self.play_button.get_rend())
        self.world.add_component(self.exit_b, self.exit_button.get_rend())
        self.world.add_component(self.play_b_msg, self.play_button.get_msg())
        self.world.add_component(self.exit_b_msg, self.exit_button.get_msg())
        # self.world.add_component(self.menu_background, self.black_background)
        
        self.menu_event_dispatcher = MenuEventDispatcher(self.play_button.rect, self.exit_button.rect)
        self.world.add_processor(Render(screen), 1)
        self.world.add_processor(self.menu_event_dispatcher, 10)


    def run(self):
        running = True
        while running:
            # A single call to world.process() will update all Processors:
            self.world.process()