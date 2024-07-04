import sys, pygame
from time import sleep
from jet import Jet
from bullet import Bullet
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from enemy import Enemy


class FighterFury:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Fighter Fury")

        # Create an instance to store game statistics
        # and a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.jet = Jet(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self._create_fleet()

        # Start Fighter Jury in an inactive state.
        self.game_active = False

        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.jet.update()
                self._update_bullets()
                self._update_enemies()

            self._update_screen()
            self.clock.tick(60)

    def _jet_hit(self):
        """Respond to the jet being hit by an enemy."""
        if self.stats.jets_left > 0:
            # Decrement jets left and update scoreboard.
            self.stats.jets_left -= 1
            self.sb.prep_jets()

            # Remove any remaining bullets and enemies.
            self.bullets.empty()
            self.enemies.empty()

            # Create a new fleet and center the jet.
            self._create_fleet()
            self.jet.center_jet()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of enemies."""
        # Spacing between enemies is one enemy height and one enemy width.
        enemy = Enemy(self)
        enemy_height, enemy_width = enemy.rect.size

        current_y, current_x = enemy_height, (
            self.settings.screen_width - 3 * enemy_width
        )
        while current_x > (21 * enemy_width):
            while current_y < (self.settings.screen_height - enemy_height):
                self._create_enemy(current_y, current_x)
                current_y += 2 * enemy_height

            # Finished a column; reset y value, and increment x value.
            current_y = enemy_height
            current_x -= 2 * enemy_width

    def _create_enemy(self, y_position, x_position):
        """Create an enemy and place it in the column."""
        new_enemy = Enemy(self)
        new_enemy.y = y_position
        new_enemy.x = x_position
        new_enemy.rect.y = y_position
        new_enemy.rect.x = x_position
        self.enemies.add(new_enemy)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Remove old bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        """Respond to any bullets and enemies that have collided."""
        # Remove any bullets and enemies that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemies)
            self.stats.score += self.settings.enemy_points
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

    def _update_enemies(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.enemies.update()

        # Look for enemy-ship collisions.
        if pygame.sprite.spritecollideany(self.jet, self.enemies):
            self._jet_hit()

        # Look for enemies hitting the left of the screen.
        self._check_enemies_left()

    def _check_fleet_edges(self):
        """Respond appropriately if any enemies have reached an edge."""
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Shift left the entire fleet and change the fleet's direction."""
        for enemy in self.enemies.sprites():
            enemy.rect.x -= self.settings.fleet_shift_left_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.jet.blitme()
        self.enemies.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()

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

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_jets()
            self.game_active = True

            # Remove any remaining bullets and enemies.
            self.bullets.empty()
            self.enemies.empty()

            # Create a new fleet and center the jet.
            self._create_fleet()
            self.jet.center_jet()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.jet.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.jet.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_enemies_left(self):
        """Check if any enemies have reached the left of the screen."""
        for enemy in self.enemies.sprites():
            if enemy.rect.left <= 0:
                # Treat this the same as if the fighter jet got hit.
                self._jet_hit()
                break


if __name__ == "__main__":
    # make a game instance, and run the game.
    ff = FighterFury()
    ff.run_game()
