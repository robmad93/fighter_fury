class Settings:
    """A class to store all settings for Fighter Fury."""

    def __init__(self):
        """Initialize the game's static settings."""

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (173, 216, 230)

        # Jet settings.
        self.jet_speed = 8.0
        self.jet_limit = 3

        # Bullet settings.
        self.bullet_speed = 10
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 8

        # Enemy settings.
        self.enemy_speed = 1.0
        self.fleet_shift_left_speed = 100
        # Fleet direction of 1 represents down; -1 represents up.
        self.fleet_direction = 1

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the enemy point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.jet_speed = 8.5
        self.bullet_speed = 10
        self.enemy_speed = 0.8

        # Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = -1

        # Scoring settings.
        self.enemy_points = 50

    def increase_speed(self):
        """Increase speed settings, no. bullets allowed, and enemy point values."""
        self.jet_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale
        self.bullets_allowed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)
