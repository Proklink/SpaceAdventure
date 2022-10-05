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
from pygame.color import THECOLORS
from button import Button
from scoreboard import Scoreboard
from directional_moving import directional_moving
from left_right_moving import left_right_moving


class Manager():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(screen, self.stats)
        self.asters = True

        self.play_button = Button(self.settings, self.screen.screen, "Play", self.screen.width / 2, self.screen.height / 2)
        self.exit_button = Button(self.settings, self.screen.screen, "Exit", self.screen.width / 2, self.screen.height / 2 + 2 * 50)
        
        self.init_game()

    def init_game(self):
        self.ship = Ship(self.screen,
                         self.settings.sh_image,
                         self.settings.sh_max_health,
                         self.settings.sh_health_bar_height,
                         self.settings.sh_health_bar_shifty,
                         self.settings.sh_lives_limit,
                         self.settings.sh_damage)
        self.direct_moving = directional_moving(self.ship,
                                                self.settings.sh_init_posx,
                                                self.settings.sh_init_posy,
                                                self.settings.sh_acceleration,
                                                self.settings.sh_max_speed,
                                                self.settings.sh_angle_speed,
                                                self.settings.sh_init_diretion)

        self.stright_moving = left_right_moving(self.ship,
                                                self.settings.sh_init_posx,
                                                self.settings.sh_init_posy,
                                                self.settings.sh_speed)

        self.ship.set_moving(self.stright_moving)

        self.bullets = Group()
        self.aliens = Group()
        self.asteroids = Group()
        self.stats.reset_stats()

        # self.create_fleet(self.settings.al_width)
    
    def destroy_game(self):
        self.bullets.empty()
        self.aliens.empty()
        self.asteroids.empty()

    def events(self):
        if self.stats.game_active:
            ge.check_events_game_active(self, self.ship, self.stats)
        else:
            ge.check_events_game_inactive(self, self.stats)
    
    def update(self):
        if self.stats.game_active:
            self.ship.update(self.bullets)
            self.ship_shooting()
            self.update_bullets()
            self.update_asteroids()

    def draw(self):
        if self.stats.game_active:
            self.draw_game_screen()
        else:
            self.draw_menu_screen()
        pygame.display.flip()

    def ship_shooting(self):
        if self.ship.shooting and self.ship.frames == 0:
            self.fire_bullet()
            self.ship.frames = self.ship.frames_per_bullet

    def switch_moving(self):
        if type(self.ship.moving_component) == directional_moving:
            self.ship.set_moving(self.stright_moving)
        else:
            self.ship.set_moving(self.direct_moving)

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
                self.stats.score += 1
            else:
                collisions[bul][0].health -= bul.damage

        collisions = pygame.sprite.groupcollide(self.bullets, self.asteroids, True, False)
        for bul in collisions:
            if collisions[bul][0].health <= bul.damage:
                self.asteroids.remove(collisions[bul][0])
                self.stats.score += 1
            else:
                collisions[bul][0].health -= bul.damage 

        self.bullets.update()

    def fire_bullet(self):
        bul = Bullet(self.screen.screen,
                     self.ship.get_current_direction(),
                     self.settings.bul_width,
                     self.settings.bul_height,
                     self.settings.bul_color,
                     self.settings.bul_speed,
                     self.settings.bul_damage,
                     self.settings.bul_image,
                     self.ship.rect.centerx,
                     self.ship.rect.centery)
        self.bullets.add(bul)

    def draw_game_screen(self):
        """Update images on the screen and flip to the new screen."""

        self.screen.screen.blit(self.screen.image, self.screen.rect)
        self.ship.blitme()
        
        for alien in self.aliens:
            alien.draw()

        for ast in self.asteroids:
            ast.draw()

        self.sb.show_scoreboard()
        self.bullets.draw(self.screen.screen)

    def draw_menu_screen(self):
        self.screen.screen.blit(self.screen.image, self.screen.rect)
        pygame.draw.rect(self.screen.screen, THECOLORS['black'], self.screen.rect)
        self.play_button.draw_button()
        self.exit_button.draw_button()


    def update_asteroids(self):
        if len(self.asteroids) == 0 and self.asters:
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
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.ship.reset_ship()
            self.ship.health = self.ship.max_health
            self.asteroids.empty()
            sleep(0.5)
        else:
            self.stats.game_active = False