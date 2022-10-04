import pygame

class Settings():
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings start
        self.scr_width = 1200
        self.scr_height = 600
        self.scr_caption = "Space Adventure"
        self.scr_background_image_path = 'images/space.jpg'
        self.scr_image = pygame.image.load(self.scr_background_image_path)
        # Screen settings end

        #ship settings start
        self.sh_image_path = 'images/ships/Ships3/ship1.png'
        self.sh_image = pygame.image.load(self.sh_image_path)
        
        self.sh_acceleration = 0.05
        self.sh_max_speed = 2

        self.sh_angle_speed = 1
        self.sh_init_diretion = [0, -1]

        self.sh_speed = 4

        self.sh_max_health = 50
        self.sh_health_bar_height = 5
        self.sh_health_bar_shifty = 6
        self.sh_lives_limit = 3

        self.sh_damage = 25

        self.sh_init_posx = self.scr_width / 2
        self.sh_init_posy = self.scr_height - self.sh_image.get_rect().height / 2
        #ship settings end

        #alien settings start
        self.al_image_path = 'images/ships/Ships1/RD1.png'
        self.al_image = pygame.image.load(self.al_image_path)
        self.al_width = self.al_image.get_rect().width
        self.al_height = self.al_image.get_rect().height

        self.al_init_rotation_angle = 180

        self.al_max_health = 500
        self.al_health_height = 5
        self.al_health_bar_shift = 6
        #alien settings end

        #asteroid settings start
        self.ast_image_path = 'images/ships/Ships1/RD1.png'
        self.ast_image = pygame.image.load(self.ast_image_path)
        self.ast_width = self.ast_image.get_rect().width
        self.ast_height = self.ast_image.get_rect().height

        self.ast_init_rotation_angle = 180

        self.ast_max_health = 50
        self.ast_health_height = 5
        self.ast_health_bar_shift = 6
        self.ast_speed = 1
        self.ast_damage = 25
        #alien settings end

        #bullet settings start
        self.bul_width = 5
        self.bul_height = 5
        self.bul_color = (255, 10, 10)
        self.bul_speed = 4
        self.bul_damage = 25
        self.bul_image = pygame.Surface((self.bul_width, self.bul_height), pygame.SRCALPHA)
        #bullet settings end
