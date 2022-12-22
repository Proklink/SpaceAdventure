from dataclasses import dataclass as component

@component
class controllable:
    def __init__(self, id):
        self.id = id