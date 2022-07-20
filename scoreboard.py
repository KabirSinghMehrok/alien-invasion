# -- STAR FIGHT --
# ====================

# _______________
# Date - 26102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

import pygame.font

from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to store scoring information"""

    def __init__(self, sf_game):
        """Initialize the scorekeeping attributes"""
        self.sf_game = sf_game
        self.screen = sf_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sf_game.settings
        self.stats = sf_game.stats

        # Font settings for storing information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # SysFont means the font stored in the system

        # Scoreboard display settings
        self.board_margin = 10

        # Prepare the initial score image
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # The bg_color is that of the screen

        # Display the score in the top left of the screen
        # With no gaps from the margins
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - self.board_margin
        # This shows the distance of the right edge from the screen
        self.score_rect.top = self.board_margin

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + (self.board_margin * 0.5)

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.sf_game)
            ship.rect.x = self.board_margin + ship_number * ship.rect.width
            ship.rect.y = self.board_margin
            self.ships.add(ship)