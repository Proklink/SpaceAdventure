import sys, pygame
from bullet import Bullet
from alien import Alien
from pygame.sprite import Group
from ship import Ship
from game_stat import GameStats
import game_events as ge
from asteroid import Asteroid
from time import sleep
import random


class Manager():
    def __init__(self, settings, screen):
        self.ship = Ship(screen,
                         settings.sh_acceleration,
                         settings.sh_max_speed,
                         settings.sh_angle_speed,
                         settings.sh_init_diretion,
                         settings.sh_image,
                         settings.sh_max_health,
                         settings.sh_health_bar_height,
                         settings.sh_health_bar_shifty,
                         settings.sh_lives_limit,
                         settings.sh_damage,
                         settings.sh_init_posx,
                         settings.sh_init_posy)
        self.bullets = Group()
        self.aliens = Group()
        self.asteroids = Group()
        self.stats = GameStats(settings)
        self.screen = screen
        self.settings = settings

        self.create_fleet(self.settings.al_width)

    def events(self):
        ge.check_events(self.ship, self.stats)
    
    def update(self):
        if self.stats.game_active:
            self.ship.update(self.bullets)
            self.update_bullets()
            self.update_asteroids()

    def draw(self):
        self.draw_screen()

    def ship_shooting(self):
        #костыль, тк проверяются данные корабля в классе менеджера
        #оставлено в таком виде, чтобы не передавать в check_events объект менеджера
        if self.ship.shooting:  
            self.fire_bullet()

    def create_fleet(self, width):
        """Create a full fleet of aliens."""

        available_space_x = self.screen.width - 2 * width
        number_aliens_x = int(available_space_x / (2 * width))

        for alien_number in range(number_aliens_x):
            alien = Alien(self.screen.screen,
                          self.settings.al_image,
                          self.settings.al_max_health,
                          self.settings.al_health_height,
                          self.settings.al_health_bar_shift)
            alien.x = width + 2 * width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)

    def update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or \
            bullet.rect.top >= self.screen.height or \
            bullet.rect.right <= 0 or \
            bullet.rect.left >= self.screen.width:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        for bul in collisions:
            if collisions[bul][0].health <= bul.damage:
                self.aliens.remove(collisions[bul][0])
                self.ship.score += 1
            else:
                collisions[bul][0].health -= bul.damage

        collisions = pygame.sprite.groupcollide(self.bullets, self.asteroids, True, False)
        for bul in collisions:
            if collisions[bul][0].health <= bul.damage:
                self.asteroids.remove(collisions[bul][0])
                self.ship.score += 1
            else:
                collisions[bul][0].health -= bul.damage 

        self.bullets.update()

    def fire_bullet(self):
        bul = Bullet(self.screen.screen,
                     self.ship.current_direction.copy(),
                     self.setting.bul_width,
                     self.setting.bul_height,
                     self.setting.bul_color,
                     self.setting.bul_speed,
                     self.setting.bul_damage,
                     self.setting.bul_image,
                     self.ship.rect.centerx,
                     self.ship.rect.centery)
        self.bullets.add(bul)

    def draw_screen(self):
        """Update images on the screen and flip to the new screen."""

        self.screen.screen.blit(self.screen.image, self.screen.rect)
        self.ship.blitme()
        
        for alien in self.aliens:
            alien.draw()

        for ast in self.asteroids:
            ast.draw()

        self.bullets.draw(self.screen)
        
        pygame.display.flip()

    def update_asteroids(self):
        if len(self.asteroids) == 0:
            self.generate_asters(self.settings.ast_width, self.settings.ast_height)

        for aster in self.asteroids.copy():
            if aster.rect.top >= self.screen.width:
                self.asteroids.remove(aster)

        collide = pygame.sprite.spritecollide(self.ship, self.asteroids, False)
        for ast in collide:
            if self.ship.health <= ast.damage:
                self.ship_hit()
            else:
                self.ship.health -= ast.damage
            self.asteroids.remove(ast)
        
        self.asteroids.update()

    def generate_asters(self, aster_width, aster_height):
        num_asteroids = random.randint(1, 20)

        start_xpos = int(0 + aster_width / 2)
        end_xpos = int(self.screen.width - aster_width / 2)  

        for i in range(num_asteroids):
            xpos = random.randint(start_xpos, end_xpos + 1)
            ypos = random.randint(0, 50)
            aster = Asteroid(xpos, -aster_height / 2 - ypos,
                             self.screen.screen,
                             self.settings.ast_max_health,
                             self.settings.ast_health_height,
                             self.settings.ast_health_bar_shift,
                             self.settings.ast_speed,
                             self.settings.ast_damage,
                             self.settings.ast_image)
            self.asteroids.add(aster)

    def ship_hit(self):
        """Respond to ship being hit by alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.ship.init_pos_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False