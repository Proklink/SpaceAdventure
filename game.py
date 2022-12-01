import pygame
from ecs.ECS import set_handler
from screen import Screen
from settings import settings
from ecs.ECS import World

from Components.movable import movable, rotary, directional, accelerating
from Components.renderable import renderable
from Components.rigid_body import rigid_body 
from Components.health import destructible, health_bar, damage

from Systems.Movement import Movement
from Systems.Rotate import Rotate
from Systems.Render import Render
from Systems.PlayerController import PlayerController
from Systems.ShiftController import ShiftController
from Systems.EventDispatcher import EventDispatcher
from Systems.DirectionController import DirectionController
from Systems.Accelerate import Accelerate
from Systems.PlayerMapCollision import PlayerMapCollision
from Systems.Collide import Collide
from Systems.ShowHealth import ShowHealth
from Systems.Damage import Damage



def run():
    pygame.init()
    # settings = Settings()
    screen = Screen(settings.scr_width,
                    settings.scr_height,
                    settings.scr_caption,
                    settings.scr_image)

    # Initialize Esper world, and create a "player" Entity with a few Components.
    world = World()
    damage_controller = Damage(world)
    player = world.create_entity()

    alien = world.create_entity()
    world.add_component(alien, renderable(settings.al_image, settings.sh_init_posx, settings.sh_init_posy - settings.scr_height / 2))
    world.add_component(alien, rigid_body(settings.al_image.get_rect(center=(settings.sh_init_posx, settings.sh_init_posy - settings.scr_height / 2)).copy()))
    world.add_component(alien, destructible(settings.al_max_health, settings.al_max_health, 1))
    world.add_component(alien, damage(25))

    world.add_component(player, movable(settings.sh_speed, settings.sh_init_diretion))
    world.add_component(player, renderable(settings.sh_image, settings.sh_init_posx, settings.sh_init_posy))
    world.add_component(player, rigid_body(settings.sh_image.get_rect(center=(settings.sh_init_posx, settings.sh_init_posy)).copy()))
    world.add_component(player, rotary(settings.sh_image.copy(), settings.sh_angle_speed))
    # world.add_component(player, directional(settings.sh_init_diretion))
    world.add_component(player, accelerating(settings.sh_acceleration, settings.sh_max_speed))
    world.add_component(player, health_bar(True, settings.sh_health_bar_shifty, settings.sh_health_bar_height))
    world.add_component(player, destructible(settings.sh_max_health, settings.sh_max_health, settings.sh_lives_limit))
    world.add_component(player, damage(settings.sh_damage))


    # Create some Processor instances, and asign them to be processed.
    world.add_processor(Movement(), 6)
    world.add_processor(Render(screen),1)
    player_contr = PlayerController(player)
    world.add_processor(player_contr, 9)
    world.add_processor(ShiftController(), 8)
    world.add_processor(EventDispatcher(player), 10)
    world.add_processor(Rotate())
    world.add_processor(Accelerate())
    # world.add_processor(DirectionController())
    world.add_processor(PlayerMapCollision(0, settings.scr_width, 0, settings.scr_height, player), 8)
    world.add_processor(Collide(0, settings.scr_width, 0, settings.scr_height), 7)
    # world.add_processor(ShowHealth(screen), 10)

    set_handler("moving_right", player_contr.right_flag)
    set_handler("moving_left", player_contr.left_flag)
    set_handler("moving_up", player_contr.up_flag)
    set_handler("moving_down", player_contr.down_flag)
    set_handler("rotate_right", player_contr.rotate_right_flag)
    set_handler("rotate_left", player_contr.rotate_left_flag)
    set_handler("shooting", player_contr.shooting_flag)
    set_handler("missile_entity_collision", damage_controller.missile_entity_collision)
    set_handler("entities_collision", damage_controller.entities_collision)

    running = True
    while running:
        # A single call to world.process() will update all Processors:
        world.process()


if __name__ == "__main__":
    run()
    pygame.quit()