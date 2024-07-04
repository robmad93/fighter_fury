import pygame
from pygame.sprite import Sprite


class Jet(Sprite):
    """A class to manage the jet."""

    def __init__(self, ff_game):
        """Initialize the jet and set its starting position."""
        super().__init__()
        self.screen = ff_game.screen
        self.screen_rect = ff_game.screen.get_rect()
        self.settings = ff_game.settings

        # Load the jet image and get its rect.
        self.image = pygame.image.load("images/fighter_jet.bmp")
        self.rect = self.image.get_rect()

        # Start each new jet at the middle left of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the jet's exact vertical position.
        self.y = float(self.rect.y)

        # Movement flags; start with a jet that's not moving.
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the jet's position based on movement flags."""

        # Ppdate the jet's y value, not the rect.
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.jet_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.jet_speed

        # Update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw the jet at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_jet(self):
        """Center the jet on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
