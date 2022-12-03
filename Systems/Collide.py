from ecs.ECS import Processor
from Components.rigid_body import rigid_body
from Components.missile import missile
from Components.health import destructible, damage
from Components.movable import movable
from ecs.ECS import dispatch_event

class Collide(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.collisions = []

    def _missile_map_collision(self, rb, mis_entity):
        if rb.collide_rect.bottom >= self.maxy or rb.collide_rect.top <= self.miny:
            self.world.delete_entity(mis_entity)
            return True
        if rb.collide_rect.left <= self.minx or rb.collide_rect.right >= self.maxx:
            self.world.delete_entity(mis_entity)
            return True
        return False

    #не давать двигаться друг в друга
    def _not_move(self, tar_entity1, tar_rb1, entity2, rb2):
        #tar_entity1 - сущность которая толкает entity2
        # CRiNF = collide rect in next frame
        mov = self.world.try_component(tar_entity1, movable)
        if not mov:
            return
        
        CRiNF = tar_rb1.collide_rect.copy()
        if mov.yshift != 0:
            CRiNF.centery += mov.yshift
        if mov.xshift != 0:
            CRiNF.centerx += mov.xshift
        
        is_x_axe = None

        if CRiNF.bottom >= rb2.collide_rect.top and CRiNF.top < rb2.collide_rect.top and mov.yshift > 0:
            mov.yshift = 0
            is_x_axe = False
        if CRiNF.top <= rb2.collide_rect.bottom and CRiNF.bottom > rb2.collide_rect.bottom and mov.yshift < 0:
            mov.yshift = 0
            is_x_axe = False
        if CRiNF.left <= rb2.collide_rect.right and CRiNF.right > rb2.collide_rect.right and mov.xshift < 0:
            mov.xshift = 0
            is_x_axe = True
        if CRiNF.right >= rb2.collide_rect.left and CRiNF.left < rb2.collide_rect.left and mov.xshift > 0:
            mov.xshift = 0
            is_x_axe = True
        return is_x_axe

    def _damage_possibility_check(self, moving_entity, moving_entity_rb1, entity2, rb2, is_x_axe):
        moving_entity_dest = self.world.try_component(moving_entity, destructible)
        moving_entity_dam = self.world.try_component(moving_entity, damage)
        entity2_dest = self.world.try_component(entity2, destructible)
        entity2_dam = self.world.try_component(entity2, damage)

        if (entity2_dest and moving_entity_dam):
            print("entities_collision dest1 and dam2")
            dispatch_event("entities_collision", moving_entity, moving_entity_rb1, moving_entity_dest, moving_entity_dam,
                                                 entity2, rb2, entity2_dest, entity2_dam,
                                                 is_x_axe)

    def _entities_collision(self, taget_rb, target_entity, comps_and_entities):
        for entity, rb in comps_and_entities:
            if entity == target_entity:
                continue
           
            collide = taget_rb.collide_rect.colliderect(rb.collide_rect)
            if not collide:
                continue
            if (target_entity, entity) in self.collisions:
                continue
            is_x_axe = self._not_move(target_entity, taget_rb, entity, rb)
            self._damage_possibility_check(target_entity, taget_rb, entity, rb, is_x_axe)
            is_x_axe = self._not_move(entity, rb, target_entity, taget_rb)
            self._damage_possibility_check(entity, rb, target_entity, taget_rb, is_x_axe)
            
            self.collisions.append((target_entity, entity))
            self.collisions.append((entity, target_entity))

    def process(self):
        comps_and_entities = list()
        self.world.get_components_for(rigid_body, comps_and_entities)

        for entity, rb in comps_and_entities:
            #check for missile collision check
            mis = self.world.try_component(entity, missile)
            if mis:
                if self._missile_map_collision(rb, entity):
                    continue
            
            self._entities_collision(rb, entity, comps_and_entities)
            


