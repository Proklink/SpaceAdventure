from ecs.ECS import Processor
from Systems.Scripts import level_1_wave_1

scripts = [
    level_1_wave_1.l_1_w_1,
]

class ScriptLoader(Processor):
    def __init__(self):
        super().__init__()
        self.current_Processor = scripts[0]


    def process(self):
        if self.current_Processor != None:
            self.world.add_processor(self.current_Processor(self.world))
            self.current_Processor = None