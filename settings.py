class Settings:
    """A class to store all settings for Fighter Fury."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (173, 216, 230)  # Light blue background (representing the sky).
        self.bullets_allowed = 5

        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)

        # Fighter jet settings
        self.fighter_jet_speed = 1.5
        self.fighter_jet_limit = 3

        # Enemy settings
        self.enemy_speed = 1.0
        self.fleet_drop_speed = 10

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the enemy point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.fighter_jet_speed = 1.5
        self.bullet_speed = 3.0
        self.enemy_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.enemy_points = 50

    def increase_speed(self):
        """Increase speed settings and enemy point values."""
        self.fighter_jet_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)

        # Check that the points increment has been successfully applied.
        # print(self.enemy_points)
