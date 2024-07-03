import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from fighter_jet import FighterJet
from bullet import Bullet
from enemy import Enemy


class FighterFury:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # Full screen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Fighter Fury")

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.fighter_jet = FighterJet(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.fighter_jet.update()
                self._update_bullets()
                self._update_enemies()

            self._update_screen()

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
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            # Move the fighter jet up.
            self.fighter_jet.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.fighter_jet.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.fighter_jet.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.fighter_jet.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and remove old bullets."""
        # pdate bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) # Test showing that bullets are removed in the terminal.
        self._check_bullet_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        """Respond to bullet-enemy collisions."""
        # Remove any bullets and enemies that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemies)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.enemies:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of enemies."""
        # Create an enemy and find the no. of enemies in a row.
        # Spacing between each enemy is equal to one enemy width.
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        available_space_x = self.settings.screen_width - (2 * enemy_width)
        number_enemies_x = available_space_x // (2 * enemy_width)

        # Determine the number of rows of enemies that fit on the screen.
        fighter_jet_height = self.fighter_jet.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * enemy_height) - fighter_jet_height
        )
        number_rows = available_space_y // (2 * enemy_height)
        # Create the full fleet of enemies.
        for row_number in range(number_rows):
            for enemy_number in range(number_enemies_x):
                self._create_enemy(enemy_number, row_number)

    def _create_enemy(self, enemy_number, row_number):
        """Create an enemy and place it in the row."""
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
        self.enemies.add(enemy)

    def _update_enemies(self):
        """Check if the fleet is at an edge, then update the positions of all enemies in the fleet."""
        self._check_fleet_edges()
        self.enemies.update()

        # Look for enemy-fighter jet collisions.
        if pygame.sprite.spritecollideany(self.fighter_jet, self.enemies):
            self._fighter_jet_hit()

        # Look for enemies hitting the bottom of the screen.
        self._check_enemies_left()

    def _check_fleet_edges(self):
        """Respond appropriately if any enemies have reached an edge."""
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.fighter_jet.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.enemies.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _fighter_jet_hit(self):
        """Respond to the fighter jet getting hit by an alien."""
        if self.stats.fighter_jets_left > 0:
            # Decrement fighter_jets_left, and update scoreboard.
            self.stats.fighter_jets_left -= 1
            self.sb.prep_fighter_jets()

            # Remove any remaining enemies and bullets.
            self.enemies.empty()
            self.bullets.empty()

            # Create a new fleet and center the fighter_jet.
            self._create_fleet()
            self.fighter_jet.center_fighter_jet()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_enemies_left(self):
        """Check if any enemies have reached the left of the screen."""
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.left >= screen_rect.left:
                # Treat this the same as if the fighter jet got hit.
                self._fighter_jet_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_fighter_jets()

        # Remove any remaining enemies & bullets.
        self.enemies.empty()
        self.bullets.empty()

        # Create a new fleet and center the fighter jet.
        self._create_fleet()
        self.fighter_jet.center_fighter_jet()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ff = FighterFury()
    ff.run_game()
