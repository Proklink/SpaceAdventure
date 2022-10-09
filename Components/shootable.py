from dataclasses import dataclass as component

@component
class shootable:
    def __init__(self, collide_rect):
        self.shooting = False
        self.frames_per_bullet = 20
        self.frames_left = 0