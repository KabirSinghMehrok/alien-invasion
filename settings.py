# -- STAR FIGHT --
# ====================

# _______________
# Date - 26102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

class Settings:
    """A class that stores all the settings in Star Flight"""

    def __init__(self):
        """Initialise the static settings"""

        # Screen settings
        self.screen_width = 600
        self.screen_height = 400
        self.bg_color = (40, 40, 40)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # Alien settings
        self.number_of_rows = 2
        # It tells the number of rows of aliens in the fleet
        # Yes, rect can take float values indirectly
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        # We will multiply the direction by -1 to change the direction of the fleet
        self.alien_space_from_edge = 0

        # Exponential increase factor
        self.speed_up_scale = 1.1
        # How quickly the alien point value increase
        self.score_scale = 1.5

        # Initialize the dynamic settings
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        """Initialize settings that change throughout the game."""
        self.ship_speed = 0.5
        self.bullet_speed = 1
        self.alien_x_speed = 0.2
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase the speed and alien point values"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_x_speed *= self.speed_up_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # We used int as the score needs to be integer but the score_scale is a float