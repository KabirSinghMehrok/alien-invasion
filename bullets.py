# -- STAR FIGHT --
# ====================

# _______________
# Date - 27102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

import pygame
from pygame.sprite import Sprite

class Bullets(Sprite):
    """A class to manage the bullets shot from spaceship"""

    def __init__(self, sf_game):
        """To create the bullet at the current ships position"""
        super().__init__()
        self.settings = sf_game.settings
        self.screen = sf_game.screen
        self.color = sf_game.settings.bullet_color

        # Create a bullet at (0, 0) and then match its midbottom with space ship's
        # SN - I was unable to do self.sf_game.settings.screen_width
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = sf_game.ship.rect.midtop

        # Store bullets position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
    # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)