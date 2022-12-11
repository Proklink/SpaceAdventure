from ecs.ECS import Processor
from common.common import timer
from settings import settings
from common.Builders import entities_generator
from Components.renderable import renderable
from Components.movable import movable


class l_1_w_1(Processor):
    def __init__(self, world):
        super().__init__()
        self.fleet = []
        self.fire_frequency = 1 #sec

        self.arg_world = world

        #можно сделать лучше
        available_space_x = settings.scr_width - 2 * settings.ast_width
        number_aliens_x = int(available_space_x / (3 * settings.ast_width))

        for alien_number in range(number_aliens_x):
            posx = settings.ast_width + 3 * settings.ast_width * alien_number
            posy = -settings.ast_height * 1.5
            al = entities_generator.add_alien(world, posx, posy)
            self.fleet.append(al)
        timer(self.fire_frequency, self.fire)

    def fire(self):
        for al in self.fleet:
            entities_generator.add_bullet(al, self.world, settings.ast_init_diretion)

        timer(self.fire_frequency, self.fire)

    def alien_update(self, al):
        rend = self.world.try_component(al, renderable)
        if rend.rect.centery >= settings.scr_height / 4:
            if self.world.has_component(al, movable):
                self.world.remove_component(al, movable)


    def process(self):
        #в этом классе  может возникнуть конфликт объекта world, который в аргументах
        #конструктора и с self.world, который будет передан методом add_processor
        #поэтому пока что бросаю исключение
        if self.arg_world != self.world:
            raise "inappropriate worlds in l_1_w_1"
        for ent in self.fleet:
            if not self.world.entity_exists(ent):
                continue
            self.alien_update(ent)