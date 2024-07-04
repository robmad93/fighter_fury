import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to represent a sinlge enemy in the fleet."""

    def __init__(self, ff_game):
        """Initialize the enemy and set its starting position."""
        super().__init__()
        self.screen = ff_game.screen
        self.settings = ff_game.settings

        # Load the enemy image and set its rect attribute.
        self.image = pygame.image.load("images/enemy.bmp")
        self.rect = self.image.get_rect()

        # Start each new enemy near the far right of the screen.
        self.rect.x = self.settings.screen_width + self.rect.width
        self.rect.y = 0 + self.rect.height

        # Store the enemy's exact vertical position.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if the enemy is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0)

    def update(self):
        """Move the enemy up or down."""
        self.y += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.y = self.y
