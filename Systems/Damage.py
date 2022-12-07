from ecs.ECS import Processor
from Components.rigid_body import rigid_body
from Components.missile import missile
from ecs.ECS import dispatch_event
from Components.health import destructible, damage
from Components.movable import movable
from math import sqrt

class Damage():
    def __init__(self, world):
        super().__init__()
        self.world = world

    def _damage(self, entity_dist_comp, entity, damage):
        if entity_dist_comp.health <= damage:
            self.world.delete_entity(entity)
            # dispatch_event("entity destroyed")
            print("entity {} destroyed ".format(entity))
        else:
            entity_dist_comp.health -= damage
            print("entity {} health {}".format( entity, entity_dist_comp.health))

    def missile_entity_collision(self, ent1, ent2):
        ent1_dist = self.world.try_component(ent1, destructible)
        ent2_dist = self.world.try_component(ent2, destructible)

        if ent1_dist and ent2_dist:
            self._damage(ent1_dist, ent1, 25)
            self._damage(ent2_dist, ent2, 25)

    def _speed_projection_module(self, reference_entity_rb, target_entity_rb, reference_entity_movable, is_x_axe):
        vector_between_entities = [target_entity_rb.collide_rect.centerx - reference_entity_rb.collide_rect.centerx,
                                   target_entity_rb.collide_rect.centery - reference_entity_rb.collide_rect.centery]
        vector_between_entities_module = sqrt(vector_between_entities[0]**2 + vector_between_entities[1]**2)
        if vector_between_entities_module == 0:
            return 0
        reference_entity_speed_vector = [0, 0]
        if is_x_axe:
            reference_entity_speed_vector[0] = reference_entity_movable.xspeed * reference_entity_movable.direction.x_sign
        else:
            reference_entity_speed_vector[1] = reference_entity_movable.yspeed * reference_entity_movable.direction.y_sign
        scalar_vectors_product = vector_between_entities[0] * reference_entity_speed_vector[0] + vector_between_entities[1] * reference_entity_speed_vector[1]

        return scalar_vectors_product / vector_between_entities_module

    def is_mis_owner(self, mis, entity):
        if mis and entity == mis.owner:
            return True
        else:
            return False

    # урон высчитывается как произведение базового урона на модуль проекции 
    # компонента вектора скорости (который направлен на целевую сущность) на вектор направления
    # от центра rigid_body сущности отсчета (entity1) на центр rigid_body целевой сущности(target_entity)
    #entity1 - сущность которая толкает target_entity
    def entities_collision(self, entity1, rb1, dest1, dam1,
                                 target_entity, target_rb, target_dest, target_dam,
                                 is_x_axe):
        mis1 = self.world.try_component(entity1, missile)
        mis_tar = self.world.try_component(target_entity, missile)
        if self.is_mis_owner(mis1, target_entity) or self.is_mis_owner(mis_tar, entity1):
            return

        mov1 = self.world.try_component(entity1, movable)
        print("entities_collision")
        if (target_dest and dam1 and mov1):
            spm = self._speed_projection_module(rb1, target_rb, mov1, is_x_axe)
            calc_damage = dam1.damage * spm
            #наносим урон как целевой сущности
            self._damage(target_dest, target_entity, calc_damage)
            #так и сущности, которая наносит урон
            if dest1:
                self._damage(dest1, entity1, calc_damage)
