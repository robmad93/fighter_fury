import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the jet."""

    def __init__(self, ff_game):
        """Create a bullet object at the jet's current position."""
        super().__init__()
        self.screen = ff_game.screen
        self.settings = ff_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midright = ff_game.jet.rect.midright

        # Store the bullet's position as a float.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet to the right on the scrren."""
        # update the exact position of the bullet
        self.x += self.settings.bullet_speed
        # update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
