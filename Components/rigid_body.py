from dataclasses import dataclass as component

@component
class rigit_body:
    def __init__(self, collide_rect):
        self.collide_rect = collide_rect

@component
class damage:
    def __init__(self, damage):
        self.damage = damage
        