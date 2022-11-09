import pygame
from screen import Screen
from settings import settings
from ecs.ECS import World
from Components.movable import movable, rotary, directional, accelerating
from Components.renderable import renderable
from Components.rigid_body import rigid_body 
from Systems.Movement import Movement
from Systems.Rotate import Rotate
from Systems.Render import Render
from Systems.PlayerController import PlayerController
from Systems.ShiftController import ShiftController
from Systems.EventDispatcher import EventDispatcher
from Systems.DirectionController import DirectionController
from Systems.Accelerate import Accelerate
from ecs.ECS import set_handler
from Systems.PlayerMapCollision import PlayerMapCollision


def run():
    pygame.init()
    # settings = Settings()
    screen = Screen(settings.scr_width,
                    settings.scr_height,
                    settings.scr_caption,
                    settings.scr_image)

    # Initialize Esper world, and create a "player" Entity with a few Components.
    world = World()
    player = world.create_entity()
    
    world.add_component(player, movable(settings.sh_speed, settings.sh_init_diretion))
    world.add_component(player, renderable(settings.sh_image, settings.sh_init_posx, settings.sh_init_posy))
    world.add_component(player, rigid_body(settings.sh_image.get_rect(center=(settings.sh_init_posx, settings.sh_init_posy)).copy()))
    world.add_component(player, rotary(settings.sh_image.copy(), settings.sh_angle_speed))
    world.add_component(player, directional(settings.sh_init_diretion))
    world.add_component(player, accelerating(settings.sh_acceleration, settings.sh_max_speed))


    # Create some Processor instances, and asign them to be processed.
    world.add_processor(Movement(), 7)
    world.add_processor(Render(screen))
    player_contr = PlayerController(player)
    world.add_processor(player_contr, 9)
    world.add_processor(ShiftController(), 8)
    world.add_processor(EventDispatcher(player), 10)
    world.add_processor(Rotate())
    world.add_processor(Accelerate())
    world.add_processor(DirectionController())
    world.add_processor(PlayerMapCollision(0, settings.scr_width, 0, settings.scr_height, player), 8)

    set_handler("moving_right", player_contr.right_flag)
    set_handler("moving_left", player_contr.left_flag)
    set_handler("moving_up", player_contr.up_flag)
    set_handler("moving_down", player_contr.down_flag)
    set_handler("rotate_right", player_contr.rotate_right_flag)
    set_handler("rotate_left", player_contr.rotate_left_flag)
    set_handler("shooting", player_contr.shooting_flag)

    running = True
    while running:
        # A single call to world.process() will update all Processors:
        world.process()


if __name__ == "__main__":
    run()
    pygame.quit()