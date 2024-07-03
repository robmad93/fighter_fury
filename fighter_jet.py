import pygame
from pygame.sprite import Sprite


class FighterJet(Sprite):
    """A class to manage the fighter jet."""

    def __init__(self, ff_game):
        """Initialize the fighter jet and set its starting position."""
        super().__init__()
        self.screen = ff_game.screen
        self.settings = ff_game.settings
        self.screen_rect = ff_game.screen.get_rect()

        # Load the fighter jet image and get its rect.
        self.image = pygame.image.load("images/fighter_jet.bmp")
        self.rect = self.image.get_rect()

        # Start each new fighter jet at the left center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the fighter jet's vertical position.
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the fighter jet's position based on movement flags."""
        # Update the jet's y value, not the rect.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.fighter_jet_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.fighter_jet_speed

        # Update rect object from self.y.
        self.rect.y = self.y

    def blitme(self):
        """Draw the fighter jet at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_fighter_jet(self):
        """Center the fighter jet on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
