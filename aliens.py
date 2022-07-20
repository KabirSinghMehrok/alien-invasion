# -- STAR FIGHT --
# ====================

# _______________
# Date - 28102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Models a single alien in the alien fleet"""
    def __init__(self, sf_game):
        super().__init__()
        self.screen = sf_game.screen
        self.settings = sf_game.settings

        # Load the image and set its rect attribute
        self.image = pygame.image.load('Images/Alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien at top left of the screen
        # With the padding of its width and height
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store exact position of the alien in float
        self.x = float(self.rect.x)

    def check_edges(self):
        """Returns True when an alien has touched the edges of the screen"""
        screen_rect = self.screen.get_rect()
        space = self.settings.alien_space_from_edge
        if self.rect.right >= (screen_rect.right - space) or self.rect.left <= space:
            return True

    def update(self):
        """Update the position of the alien"""
        self.x += (self.settings.alien_x_speed * self.settings.fleet_direction)
        self.rect.x = self.x
