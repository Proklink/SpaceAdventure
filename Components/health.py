from dataclasses import dataclass as component

@component
class destructible:
    def __init__(self, health, max_health, lives_limit):
        self.health = health
        self.max_health = max_health
        self.lives_limit = lives_limit

@component
class health_bar:
    def __init__(self, is_top, shift_from_object, health_bar_height):
        self.is_top = is_top
        self.shift_from_object = shift_from_object
        self.height = health_bar_height

@component
class damage:
    def __init__(self, damage):
        self.damage = damage