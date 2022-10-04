import sys, pygame


def check_keydown_events(event, ship):
    if event.key == pygame.K_e:
        ship.moving_right = True
    if event.key == pygame.K_q:
        ship.moving_left = True
    if event.key == pygame.K_w:
        ship.moving_up = True
    if event.key == pygame.K_s:
        ship.moving_down = True

    if event.key == pygame.K_d:
        ship.rotate_right = True
    if event.key == pygame.K_a:
        ship.rotate_left = True

    if event.key == pygame.K_SPACE:
        ship.shooting = True

def check_keyup_events(event, ship):
    if event.key == pygame.K_e:
        ship.moving_right = False
    if event.key == pygame.K_q:
        ship.moving_left = False
    if event.key == pygame.K_w:
        ship.moving_up = False
    if event.key == pygame.K_s:
        ship.moving_down = False

    if event.key == pygame.K_d:
        ship.rotate_right = False
    if event.key == pygame.K_a:
        ship.rotate_left = False

    if event.key == pygame.K_SPACE:
        ship.shooting = False

def game_activation(stats):
    if stats.game_active:
        stats.game_active = False
    else:
        stats.game_active = True

def check_events(ship, stats):
    """Respond to keypresses and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
            if event.key == pygame.K_ESCAPE:
                game_activation(stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)