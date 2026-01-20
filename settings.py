import pygame
import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
SKINS_DIR = os.path.join(ASSETS_DIR, "skins")

# Game Settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Flappy Bird - Ultimate Edition v2.0"

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_SHOP = "shop"
STATE_SETTINGS = "settings"

# Colors - Modern Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

# UI Colors
PRIMARY_COLOR = (255, 198, 51)       # Golden yellow
SECONDARY_COLOR = (83, 189, 149)      # Mint green
ACCENT_COLOR = (255, 107, 107)        # Coral red
DARK_OVERLAY = (0, 0, 0, 180)         # Semi-transparent black
PANEL_COLOR = (222, 184, 135)         # Tan/wood color
PANEL_DARK = (139, 90, 43)            # Dark wood
TEXT_SHADOW = (50, 50, 50)            # Shadow color
COIN_COLOR = (255, 215, 0)            # Gold for coins

# Gradient colors for background
SKY_TOP = (135, 206, 250)             # Light sky blue
SKY_BOTTOM = (176, 224, 230)          # Powder blue

# Difficulty Settings
DIFFICULTIES = {
    "easy": {
        "gravity": 0.20,
        "jump": -4.5,
        "scroll_speed": 2.5,
        "pipe_gap": 180,
        "pipe_frequency": 2000,
        "coin_frequency": 3000
    },
    "medium": {
        "gravity": 0.25,
        "jump": -5,
        "scroll_speed": 3,
        "pipe_gap": 150,
        "pipe_frequency": 1500,
        "coin_frequency": 2500
    },
    "hard": {
        "gravity": 0.30,
        "jump": -5.5,
        "scroll_speed": 4,
        "pipe_gap": 120,
        "pipe_frequency": 1200,
        "coin_frequency": 2000
    }
}

# Default difficulty
CURRENT_DIFFICULTY = "medium"

# Physics (default - will be overridden by difficulty)
GRAVITY = 0.25
BIRD_JUMP = -5
SCROLL_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Ground settings
GROUND_HEIGHT = 80

# Medal Thresholds
MEDAL_THRESHOLDS = {
    "bronze": 5,
    "silver": 15,
    "gold": 30,
    "platinum": 50
}

# Bird Settings
BIRD_WIDTH = 45
BIRD_HEIGHT = 35
BIRD_ANIMATION_SPEED = 150  # ms per frame

# Pipe Settings
PIPE_WIDTH = 52
PIPE_MIN_HEIGHT = 50

# Coin Settings
COIN_SIZE = 30
COIN_VALUE = 1

# Power-up Settings
POWERUP_SIZE = 35
POWERUP_DURATION = 5000  # 5 seconds

# Particle Settings
PARTICLE_COUNT = 15
PARTICLE_LIFETIME = 500  # ms

# Font sizes
FONT_LARGE = 48
FONT_MEDIUM = 32
FONT_SMALL = 24
FONT_TINY = 18

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_RADIUS = 10

# Animation settings
FADE_SPEED = 8  # Alpha change per frame
TRANSITION_SPEED = 15

# Score file
SCORE_FILE = os.path.join(BASE_DIR, "highscore.json")
DATA_FILE = os.path.join(BASE_DIR, "gamedata.json")

# Skin definitions - ID: (name, price, description, special_ability)
SKINS = {
    "default": {
        "name": "Classic",
        "price": 0,
        "description": "The original flappy bird",
        "ability": None,
        "unlocked": True
    },
    "red_angry": {
        "name": "Angry Red",
        "price": 50,
        "description": "Furious and fast!",
        "ability": None,
        "unlocked": False
    },
    "blue_ice": {
        "name": "Ice Bird",
        "price": 100,
        "description": "Cool as ice",
        "ability": "slow_time",
        "unlocked": False
    },
    "pink_love": {
        "name": "Lovely Pink",
        "price": 75,
        "description": "Spread the love!",
        "ability": None,
        "unlocked": False
    },
    "ninja": {
        "name": "Ninja Bird",
        "price": 150,
        "description": "Silent but deadly",
        "ability": "double_coins",
        "unlocked": False
    },
    "robot": {
        "name": "Robo Bird",
        "price": 200,
        "description": "Upgraded with tech",
        "ability": "shield",
        "unlocked": False
    },
    "golden": {
        "name": "Golden King",
        "price": 500,
        "description": "The richest bird!",
        "ability": "coin_magnet",
        "unlocked": False
    },
    "zombie": {
        "name": "Zombie Bird",
        "price": 120,
        "description": "Back from the dead",
        "ability": "extra_life",
        "unlocked": False
    },
    "rainbow": {
        "name": "Rainbow",
        "price": 250,
        "description": "Magical colors!",
        "ability": "score_boost",
        "unlocked": False
    },
    "fire": {
        "name": "Phoenix",
        "price": 300,
        "description": "Born from flames",
        "ability": "invincible",
        "unlocked": False
    },
    "galaxy": {
        "name": "Cosmic",
        "price": 400,
        "description": "From another dimension",
        "ability": "teleport",
        "unlocked": False
    }
}

# Power-up types
POWERUPS = {
    "shield": {
        "name": "Shield",
        "duration": 5000,
        "color": (100, 200, 255)
    },
    "coin_magnet": {
        "name": "Coin Magnet",
        "duration": 8000,
        "color": (255, 50, 50)
    },
    "slow_time": {
        "name": "Slow Motion",
        "duration": 4000,
        "color": (150, 150, 255)
    },
    "score_boost": {
        "name": "2x Score",
        "duration": 10000,
        "color": (255, 215, 0)
    }
}

# Combo system
COMBO_THRESHOLD = 3  # Pipes to pass for combo
COMBO_MULTIPLIER = 1.5
