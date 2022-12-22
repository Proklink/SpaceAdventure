from ecs.ECS import Processor
from ecs.ECS import set_handler
from Systems.Scripts import level_1_wave_1

scripts = [
    level_1_wave_1.l_1_w_1,
]

class ScriptLoader(Processor):
    def __init__(self):
        super().__init__()
        self.current_script = None
        set_handler("scripts_asyncs", self.asyncs)
        

    def asyncs(self, value):
        if self.current_script != None:
            self.current_script.asyncs(value)

    def process(self):
        if self.current_script == None:
            self.current_script = scripts[0](self.world)
            self.world.add_processor(self.current_script)
            