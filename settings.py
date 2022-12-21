import pygame
from pygame.transform import smoothscale

class Settings():
    """Initialize the game's settings."""
    # Screen settings start
    scr_width = 1200
    scr_height = 600
    scr_caption = "Space Adventure"
    scr_background_image_path = 'images/space.jpg'
    scr_image = pygame.image.load(scr_background_image_path)
    # Screen settings end

    #ship settings start
    sh_image_path = 'images/ships/Ships3/ship1.png'
    sh_image = pygame.image.load(sh_image_path)
    sh_rect = sh_image.get_rect()
    sh_image = smoothscale(sh_image, (sh_rect.width / 6, sh_rect.height / 6))
    
    sh_acceleration = 0.01
    sh_max_speed = 1

    sh_angle_speed = 1
    sh_init_diretion = [0, -1]

    sh_speed = 1

    sh_max_health = 100
    sh_health_bar_height = 5
    sh_health_bar_shifty = 6
    sh_lives_limit = 3

    sh_damage = 25

    sh_init_posx = scr_width / 2
    sh_init_posy = scr_height - sh_image.get_rect().height / 2 - 20
    #ship settings end

    #alien settings start
    al_image_path = 'images/ships/Ships1/RD1.png'
    al_image = pygame.image.load(al_image_path)
    al_width = al_image.get_rect().width
    al_height = al_image.get_rect().height

    al_init_rotation_angle = 180

    al_max_health = 500
    al_health_height = 5
    al_health_bar_shift = 6
    al_live_limit = 1
    
    al_speed = 1
    al_damage = 25
    #alien settings end

    #asteroid settings start
    ast_image_path = 'images/ships/Ships1/RD1.png'
    ast_image = pygame.image.load(ast_image_path)
    ast_rect = ast_image.get_rect()
    ast_image = smoothscale(ast_image, (ast_rect.width / 6, ast_rect.height / 6))
    ast_width = ast_image.get_rect().width
    ast_height = ast_image.get_rect().height

    ast_init_rotation_angle = 180

    ast_init_diretion = [0, 1]

    ast_max_health = 25
    ast_live_limit = 1
    ast_health_height = 5
    ast_health_bar_shift = 6
    ast_speed = 0.5
    ast_damage = 25
    #asteroid settings end

    #bullet settings start
    bul_width = 8
    bul_height = 8
    bul_color = (255, 10, 10)
    bul_speed = 4
    bul_damage = 25
    bul_image = pygame.Surface((bul_width, bul_height), pygame.SRCALPHA)
    pygame.draw.ellipse(bul_image, bul_color, (0, 0, bul_width, bul_height))
    bul_lives_limit = 1
    bul_health = 1
    #bullet settings end

    #button settings start
    but_width = 200
    but_height = 50
    but_color = (0, 255, 0)
    but_text_color = (255, 255, 255)
    but_image = pygame.Surface((but_width, but_height), pygame.SRCALPHA)
    pygame.draw.rect(but_image, but_color, (0, 0, but_width, but_height))
    #button settings end

    #menu_background start
    mb_color = (0, 0, 0)
    mb_image = pygame.Surface((scr_width, scr_height), pygame.SRCALPHA)
    pygame.draw.rect(mb_image, mb_color, (0, 0, scr_width, scr_height))
    #menu_background end

settings = Settings()