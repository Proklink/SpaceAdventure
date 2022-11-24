from dataclasses import dataclass as component


@component
class missile:
    def __init__(self, owner_id):
        self.owner = owner_id