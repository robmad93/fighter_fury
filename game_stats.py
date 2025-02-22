class GameStats:
    """Track statistics for Fighter Fury."""

    def __init__(self, ff_game):
        """Initializes statistics."""
        self.settings = ff_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.jets_left = self.settings.jet_limit
        self.score = 0
        self.level = 1
