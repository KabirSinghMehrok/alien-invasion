# -- STAR FIGHT --
# ====================

# _______________
# Date - 26102020
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

import sys
import pygame

from ship import Ship
from bullets import Bullets
from aliens import Alien
from button import Button
from settings import Settings
from gamestats import GameStats
from scoreboard import Scoreboard
from time import sleep


class StarFight:
    """Class to manage game behaviour"""
    def __init__(self):
        """Initialize the game and create its resources"""
        pygame.init()
        # Initializes the game to work properly

        # attributes the settings
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # Object associated with self.screen is called surface

        # Create an instance of stats and of scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # attributes the ship
        self.ship = Ship(self)
        # I had to fill self here because Ship has parameter 'sf_game'

        # attributes the bullets
        self.bullets = pygame.sprite.Group()

        # attributes the aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        pygame.display.set_caption("Star Fight")

    def run_game(self):
        """Start the main loop of the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update_position()
                self._update_bullets()
                self._update_alien()

            self._update_screen()
            # They both signify helper methods
            # Helper methods do not need to be before the class
            # Neither they need to be initialised into the game

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._play_button_clicked(mouse_pos)

    # If we do not use event parameter it shows error
    # Unresolved reference 'event'
    # Maybe because it is not directly under the 'for loop'
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_F4:
            sys.exit()
        elif event.key == pygame.K_SPACE or event.key == pygame.K_z:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _play_button_clicked(self, mouse_pos):
        """Start a new game when the player hits play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()


    # Creating a fleet __init__
    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Makes an alien
        alien = Alien(self)
        alien_width = alien.rect.width

        # Judges the number of aliens that can fit
        # |-> Space between two aliens is one alien width
        available_space = self.settings.screen_width - 2 * (alien_width)
        number_of_aliens = available_space // (2 * alien_width)
        # Also added here is the attribute number of rows of alien fleet which is in settings.py

        # Creating a fleet of aliens
        for row_number in range(self.settings.number_of_rows):
            for alien_number in range(number_of_aliens):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # If alien.rect.width is used, error occurs
        # ⚠ TypeError: cannot unpack non-iterable int object

        # Setting the x position of the alien
        alien.x = alien_width * (1 + (2 * alien_number))
        alien.rect.x = alien.x

        # Setting the y position of the alien /done at the same pattern as above/
        alien.y = alien_height * (1 + (2 * row_number))
        alien.rect.y = alien.y

        # And finally adding the alien to the aliens /a type of sprite/
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond if an alien has hit the edge in the fleet"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and chnage the x direction of the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_alien(self):
        """Check the edges of the alien, change the direction and drop
        Updates the position of all the aliens in the fleet"""
        # This is possible due ot 'aliens' being a list of aliens
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for alien reaching the screen end
        self._check_alien_bottom()

    def _fire_bullet(self):
        """Create new bullet and add it to bullet group"""
        if len(self.bullets) <= self.settings.bullets_allowed:
            # Limits the number of bullets that can be on the screen at a time
            new_Bullet = Bullets(self)
            self.bullets.add(new_Bullet)

    def _update_bullets(self):
        """Gets rid of bullets"""
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) shows how many bullets are currently on the screen

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check the collision b/w bullet and aliens
        Remove those collided aliens and create a new fleet when all aliens are dead"""
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
        # The prep_score gets update here and now

        if not self.aliens:
            # Destroy the existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_alien_bottom(self):
        """Checks whether aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat as if the ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Responds to a ship being hit by an alien"""
        if self.stats.ship_left > 0:
            # Decrement the ships left
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Get rid of any aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause the game for some time
            sleep(0.5)

        else:
            self.stats.game_active = False

    def _update_screen(self):
        # Refill screen while passing through the loop
        self.screen.fill(self.settings.bg_color)
        # Print the ship after background has been filled

        # Updates ship's position
        self.ship.blitme()

        # Show aliens
        self.aliens.draw(self.screen)

        # Show score after aliens
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Show bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    sf = StarFight()
    sf.run_game()