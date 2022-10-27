import pygame.font

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen.screen

        self.screen_rect = self.screen.get_rect()
        self.bg_color = (0, 255, 0)
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare the initial score image.
        self.prep_score()
        self.prep_lives()

    def prep_score(self):
        """Turn the score into a rendered image."""

        score_str = "Score: " + str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_lives(self):
        """Turn the score into a rendered image."""

        lives_str = "Lives: " + str(self.stats.ships_left)
        self.lives_image = self.font.render(lives_str, True, self.text_color, self.bg_color)

        # Display the score at the top right of the screen.
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.right = self.screen_rect.right - 20
        self.lives_rect.top = self.score_rect.height + 20

    def show_scoreboard(self):
        """Draw score to the screen."""
        self.prep_score()
        self.prep_lives()
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.lives_image, self.lives_rect)