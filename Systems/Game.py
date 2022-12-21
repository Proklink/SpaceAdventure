from Systems.Movement import Movement
from Systems.Rotate import Rotate
from Systems.Render import Render
from Systems.ShiftController import ShiftController
from Systems.Accelerate import Accelerate
from Systems.Collide import Collide
from Systems.ShowHealth import ShowHealth
from Systems.Damage import Damage
from Systems.ScriptsLoader import ScriptLoader
from ecs.ECS import World
from common.Builders import entities_generator
from Systems.EventDispatcher import EventDispatcher
from settings import settings
from ecs.ECS import set_handler

class Game:
    def __init__(self, screen):
        self.world = World()
        self.damage_controller = Damage(self.world)
        player = entities_generator.add_player(self.world)
        self.game_event_dispatcher = EventDispatcher(player)

        # Create some Processor instances, and asign them to be processed.
        self.world.add_processor(Movement(), 6)
        self.world.add_processor(ShiftController(), 8)
        self.world.add_processor(Rotate())
        self.world.add_processor(Accelerate())
        self.world.add_processor(Collide(0, settings.scr_width, 0, settings.scr_height), 7)
        self.world.add_processor(Render(screen),1)
        self.world.add_processor(self.game_event_dispatcher, 10)
        # self.world.add_processor(ScriptLoader())

        set_handler("missile_entity_collision", self.damage_controller.missile_entity_collision)
        set_handler("entities_collision", self.damage_controller.entities_collision)

    def run(self):
        running = True
        while running:
            # A single call to world.process() will update all Processors:
            self.world.process()