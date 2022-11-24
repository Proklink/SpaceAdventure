from ecs.ECS import Processor
from Components.rigid_body import rigid_body
from Components.missile import missile
from ecs.ECS import dispatch_event
from Components.health import destructible, damage

class Damage():
    def __init__(self, world):
        super().__init__()
        self.world = world

    def _damage(self, entity_dist_comp, entity, damage):
        if entity_dist_comp.health <= damage:
            self.world.delete_entity(entity)
            # dispatch_event("entity destroyed")
            print("entity destroyed ", entity)
        else:
            entity_dist_comp.health -= damage

    def missile_entity_collision(self, ent1, ent2):
        ent1_dist = self.world.try_component(ent1, destructible)
        ent2_dist = self.world.try_component(ent2, destructible)

        if ent1_dist and ent2_dist:
            self._damage(ent1_dist, ent1, 25)
            self._damage(ent2_dist, ent2, 25)

