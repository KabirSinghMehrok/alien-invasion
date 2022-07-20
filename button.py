# -- STAR FIGHT --
# ====================

# _______________
# Date - 28102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

import pygame

class Button:

    def __init__(self, sf_game, msg):
        """Initialize the button attributes"""
        self.screen = sf_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the properties and the dimensions of the button
        self.width, self.height = 200, 50
        self.button_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Build the buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message need to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn message into a rendered image and center it on button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
