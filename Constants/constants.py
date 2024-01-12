class GameConstants:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameConstants, cls).__new__(cls)
            # Initialize your constants here
            cls.ROWS = 15
            cls.COLS = 15
            cls.TILE_SIZE = 48
            cls.SIDE_PANEL = 300
            cls.SCREEN_WIDTH = cls.TILE_SIZE * cls.COLS
            cls.SCREEN_HEIGHT = cls.TILE_SIZE * cls.ROWS
            cls.FPS = 60
            cls.HEALTH = 100
            cls.MONEY = 650
            cls.TOTAL_LEVELS = 15

            # Enemy constants
            cls.SPAWN_COOLDOWN = 400

            # Turret constants
            cls.TURRET_LEVELS = 4
            cls.BUY_COST = 200
            cls.UPGRADE_COST = 100
            cls.KILL_REWARD = 1
            cls.LEVEL_COMPLETE_REWARD = 100
            cls.ANIMATION_STEPS = 8
            cls.ANIMATION_DELAY = 15
            cls.DAMAGE = 5
        return cls._instance

# ROWS = 15
# COLS = 15
# TILE_SIZE = 48
# SIDE_PANEL = 300
# SCREEN_WIDTH = TILE_SIZE * COLS
# SCREEN_HEIGHT = TILE_SIZE * ROWS
# FPS = 60
# HEALTH = 100
# MONEY = 650
# TOTAL_LEVELS = 15

# #enemy constants
# SPAWN_COOLDOWN = 400

# #turret constants
# TURRET_LEVELS = 4
# BUY_COST = 200
# UPGRADE_COST = 100
# KILL_REWARD = 1
# LEVEL_COMPLETE_REWARD = 100
# ANIMATION_STEPS = 8
# ANIMATION_DELAY = 15
# DAMAGE = 5