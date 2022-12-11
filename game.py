import pygame
from ecs.ECS import set_handler
from screen import Screen
from settings import settings
from ecs.ECS import World

from Systems.Movement import Movement
from Systems.Rotate import Rotate
from Systems.Render import Render
from Systems.ShiftController import ShiftController
from Systems.Accelerate import Accelerate
from Systems.Collide import Collide
from Systems.ShowHealth import ShowHealth
from Systems.Damage import Damage
from Systems.ScriptsLoader import ScriptLoader

from common.Builders import entities_generator

def run():
    pygame.init()

    screen = Screen(settings.scr_width,
                    settings.scr_height,
                    settings.scr_caption,
                    settings.scr_image)

    world = World()

    damage_controller = Damage(world)
    entities_generator.add_player(world)
    # entities_generator.add_static_alien(world)

    # Create some Processor instances, and asign them to be processed.
    world.add_processor(Movement(), 6)
    world.add_processor(Render(screen),1)
    world.add_processor(ShiftController(), 8)
    world.add_processor(Rotate())
    world.add_processor(Accelerate())
    world.add_processor(Collide(0, settings.scr_width, 0, settings.scr_height), 7)
    world.add_processor(ScriptLoader())

    set_handler("missile_entity_collision", damage_controller.missile_entity_collision)
    set_handler("entities_collision", damage_controller.entities_collision)


    running = True
    while running:
        # A single call to world.process() will update all Processors:
        world.process()


if __name__ == "__main__":
    run()
    pygame.quit()