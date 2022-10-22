from ecs.ECS import Processor
from Components.rigid_body import rigid_body


class Collide(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #get_components надо протестировать на отсутствие rigid_body
        for ent, (rb) in self.world.get_component(rigid_body):
            pass