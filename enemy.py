import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to represent a single enemy."""

    def __init__(self, ff_game):
        """Initialize the enemy and set its starting position."""
        super().__init__()
        self.screen = ff_game.screen
        self.settings = ff_game.settings

        # Load the enemy image and set its rect attribute.
        self.image = pygame.image.load("images/enemy_plane.bmp")
        self.rect = self.image.get_rect()

        # Start each new enemy near the top right of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the enemy's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if enemy is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the enemy to the top or bottom."""
        self.x += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.x = self.x
