from ecs.ECS import Processor
from Components.rigid_body import rigid_body
from Components.missile import missile
from ecs.ECS import dispatch_event

class Collide(Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def _missile_map_collision(self, rb, mis_entity):
        if rb.collide_rect.bottom >= self.maxy or rb.collide_rect.top <= self.miny:
            self.world.delete_entity(mis_entity)
            return True
        if rb.collide_rect.left <= self.minx or rb.collide_rect.right >= self.maxx:
            self.world.delete_entity(mis_entity)
            return True
        return False

    def _missile_entity_collision(self, mis_component, mis_rb, mis_entity, comps_and_entities):
        for entity, rb in comps_and_entities:
            if entity == mis_entity:
                continue
           
            collide = mis_rb.collide_rect.colliderect(rb.collide_rect)
            if not collide:
                continue
            if mis_component.owner == entity:
                continue
            dispatch_event("missile_entity_collision", entity, mis_entity)


    def process(self):
        comps_and_entities = list()
        self.world.get_components_for(rigid_body, comps_and_entities)

        for entity, rb in comps_and_entities:
            #check for missile collision check
            mis = self.world.try_component(entity, missile)
            if mis:
                if self._missile_map_collision(rb, entity):
                    continue
                self._missile_entity_collision(mis, rb, entity, comps_and_entities)

            


