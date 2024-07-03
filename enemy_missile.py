import pygame
from pygame.sprite import Sprite


class EnemyMissile(Sprite):
    """A class to manage missiles fired from the enemy planes."""

    def __init__(self, ff_game, enemy):
        """Initialize the missile and set its starting position."""
        super().__init__()
        self.screen = ff_game.screen
        self.settings = ff_game.settings

        # Set the missile's dimensions and color.
        self.width = 8
        self.height = 2
        self.color = (255, 0, 0)  # Red color, adjust as needed

        # Create a rect for the missile at the enemy's current position.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midright = enemy.rect.midleft

        # Store the missile's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the missile left across the screen."""
        # Update the decimal position of the missile.
        self.x -= self.settings.enemy_bullet_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_missile(self):
        """Draw the missile to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
