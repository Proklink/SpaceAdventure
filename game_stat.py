class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, settings):
        """Initialize statistics."""

        self.ship_lives_limit = settings.sh_lives_limit
        self.game_active = True
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""

        self.ships_left = self.ship_lives_limit