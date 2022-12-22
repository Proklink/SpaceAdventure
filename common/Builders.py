from settings import settings
from ecs.ECS import set_handler

from Components.movable import movable, rotary, directional, accelerating
from Components.renderable import renderable
from Components.rigid_body import rigid_body 
from Components.health import destructible, health_bar, damage
from Components.missile import missile

from Systems.PlayerController import PlayerController

from Systems.PlayerMapCollision import PlayerMapCollision
from Systems.DirectionController import DirectionController

'''
идея со строителями мне пока не нравится: для каждой сущности свой класс кажется как то нелогичным
и кода много становится.  к тому же каждый строитель имеет только методы, которые точно все выполнятся
class Builder:
    def __init__(self):
        self.components = []
        self.posx = 0
        self.posy = 0

    def reset(self):
        self.components = []
        self.posx = 0
        self.posy = 0

    def apply(self, world):
        id = world.create_entity()
        for comp in self.components:
            world.add_component(id, comp)
        self.reset()
        return id

class AlienBuilder(Builder):
    def __init__(self):
        self.image = settings.al_image
        self.width = settings.al_width
        self.height = settings.al_height
        self.init_rotation_angle = settings.al_init_rotation_angle
        self.max_health = settings.al_max_health
        self.health_height = settings.al_health_height
        self.health_bar_shift = settings.al_health_bar_shift
        self.speed = settings.al_speed
        self.damage = settings.al_damage
        self.live_limit = settings.al_live_limit

    def _add_renderable(self, posx, posy):
        self.components.append(renderable(self.image, posx, posy))
        self.posx = posx
        self.posy = posy

    def _add_rigid_body(self):
        self.components.append(rigid_body(self.image.get_rect(center=(self.posx, self.posy)).copy()))

    def _add_destructible(self):
        self.components.append(destructible(self.max_health, self.max_health, self.live_limit))

    def _add_damage(self):
        self.components.append(damage(self.damage))

    def _add_movable(self):
        pass

    def _add_health_bar(self):
        pass

class AsteroidBuilder:
    def __init__(self):
        self.image = settings.ast_image
        self.width = settings.ast_width
        self.height = settings.ast_height
        self.init_rotation_angle = settings.ast_init_rotation_angle
        self.max_health = settings.ast_health_height
        self.health_height = settings.ast_health_bar_shift
        self.health_bar_shift = settings.al_health_bar_shift
        self.speed = settings.ast_speed
        self.damage = settings.ast_damage

class PlayerBuilder:
    pass

class BulletBuilder(Builder):
    def __init__(self):
        self.image = settings.bul_image

        self.speed = settings.bul_speed
        self.damage = settings.bul_damage
        self.live_limit = settings.bul_lives_limit

        self.max_health = settings.bul_health

    def _add_renderable(self, posx, posy):
        self.components.append(renderable(self.image, posx, posy))
        self.posx = posx
        self.posy = posy

    def _add_rigid_body(self):
        self.components.append(rigid_body(self.image.get_rect(center=(self.posx, self.posy)).copy()))

    def _add_destructible(self):
        self.components.append(destructible(self.max_health, self.max_health, self.live_limit))

    def _add_damage(self):
        self.components.append(damage(self.damage))

    def _add_movable(self, direction):
        self.components.append(movable(self.speed, direction.copy(), self.speed))

    def _add_health_bar(self):
        pass
'''


class EntitiesGenerator:
    def add_alien(self, world, posx, posy):
        alien = world.create_entity()

        world.add_component(alien, renderable(settings.ast_image, posx, posy))
        world.add_component(alien, rigid_body(settings.ast_image.get_rect(center=(posx, posy)).copy()))
        world.add_component(alien, destructible(settings.ast_max_health, settings.ast_max_health, settings.ast_live_limit))
        world.add_component(alien, damage(settings.ast_damage))
        world.add_component(alien, movable(settings.ast_speed, settings.ast_init_diretion, settings.ast_speed))
        return alien

    def add_static_alien(self, world):
        alien = world.create_entity()
        posx = settings.sh_init_posx
        posy = settings.sh_init_posy - settings.scr_height / 2

        world.add_component(alien, renderable(settings.al_image, posx, posy))
        world.add_component(alien, rigid_body(settings.al_image.get_rect(center=(posx, posy)).copy()))
        world.add_component(alien, destructible(settings.al_max_health, settings.al_max_health, settings.al_live_limit))
        world.add_component(alien, damage(settings.al_damage))

    def add_player(self, world):
        player = world.create_entity()
        posx = settings.sh_init_posx
        posy = settings.sh_init_posy
        init_dir = settings.sh_init_diretion
        shifty = settings.sh_health_bar_shifty
        bar_h = settings.sh_health_bar_height
        health = settings.sh_max_health
        col_rect = settings.sh_image.get_rect(center=(posx, posy)).copy()
        player_contr = PlayerController(player, self.add_bullet)

        world.add_component(player, movable(settings.sh_speed, init_dir))
        world.add_component(player, renderable(settings.sh_image, posx, posy))
        world.add_component(player, rigid_body(col_rect))
        world.add_component(player, rotary(settings.sh_image.copy(), settings.sh_angle_speed))
        # world.add_component(player, directional(init_dir))
        world.add_component(player, accelerating(settings.sh_acceleration, settings.sh_max_speed))
        world.add_component(player, health_bar(shifty, bar_h, col_rect.top, col_rect.left, col_rect.width))
        world.add_component(player, destructible(health, health, settings.sh_lives_limit))
        world.add_component(player, damage(settings.sh_damage))

        world.add_processor(player_contr, 9)
        world.add_processor(PlayerMapCollision(0, settings.scr_width, 0, settings.scr_height, player), 7)
        # world.add_processor(DirectionController())

        set_handler("moving_right", player_contr.right_flag)
        set_handler("moving_left", player_contr.left_flag)
        set_handler("moving_up", player_contr.up_flag)
        set_handler("moving_down", player_contr.down_flag)
        set_handler("rotate_right", player_contr.rotate_right_flag)
        set_handler("rotate_left", player_contr.rotate_left_flag)
        set_handler("shooting", player_contr.shooting_flag)
        return player


    def add_bullet(self, owner, world, fire_direction=None):
        if not world.entity_exists(owner):
            return
        rend = world.try_component(owner, renderable)
        if not rend:
            return
        bullet = world.create_entity()
        
        
        if fire_direction:
            direction = fire_direction
        else:
            dir = world.try_component(owner, directional)
            if dir:
                direction = dir.move_up_dir
            else:
                direction = [0, -1]

        bullet_mov = movable(settings.bul_speed, direction.copy(), settings.bul_speed)
        world.add_component(bullet, bullet_mov)
        world.add_component(bullet, renderable(settings.bul_image.copy(), rend.rect.centerx, rend.rect.centery))
        world.add_component(bullet, rigid_body(settings.bul_image.get_rect(center=(rend.rect.centerx, rend.rect.centery)).copy()))
        world.add_component(bullet, missile(owner))
        world.add_component(bullet, destructible(settings.bul_health, settings.bul_health, settings.bul_lives_limit))
        world.add_component(bullet, damage(settings.bul_damage))

entities_generator = EntitiesGenerator()