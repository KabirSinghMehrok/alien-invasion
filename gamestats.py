# -- STAR FIGHT --
# ====================

# _______________
# Date - 26102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

class GameStats:
    """Track the statistics of the Star Fight"""

    def __init__(self, sf_game):
        """Initialize and reset the statistics"""
        self.settings = sf_game.settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        """Initialize the statistics that can change during the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1