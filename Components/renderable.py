from dataclasses import dataclass as component

@component
class renderable:
    def __init__(self, image, init_posx, init_poxy):
        self.image = image
        self.rect = image.get_rect()
        self.init_posx = init_posx
        self.init_poxy = init_poxy
        self.rect.centerx = init_posx
        self.rect.centery = init_poxy

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)