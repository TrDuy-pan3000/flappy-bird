import pygame
import os
from datetime import datetime

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
SKINS_DIR = os.path.join(ASSETS_DIR, "skins")

# =============================================================================
# TẾT NGUYÊN ĐÁN 2026 - SPECIAL EDITION
# =============================================================================

# Check if it's Tet season (January 15 - February 15)
def is_tet_season():
    now = datetime.now()
    month = now.month
    day = now.day
    return (month == 1 and day >= 15) or (month == 2 and day <= 15) or True  # Always Tet for testing

TET_MODE = is_tet_season()

# Game Settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Flappy Bird - Tết Nguyên Đán 2026 🧧" if TET_MODE else "Flappy Bird - Ultimate Edition v2.0"
VERSION = "3.0 - Tet Edition" if TET_MODE else "2.0"

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_SHOP = "shop"
STATE_SETTINGS = "settings"

# =============================================================================
# TET COLORS - Traditional Vietnamese Lunar New Year Palette
# =============================================================================

if TET_MODE:
    # Tet Red & Gold Theme
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SKY_BLUE = (25, 25, 50)  # Night sky for Tet
    
    # UI Colors - Tet Edition
    PRIMARY_COLOR = (255, 215, 0)         # Bright Gold (Vàng Kim)
    SECONDARY_COLOR = (200, 30, 30)       # Lucky Red (Đỏ May Mắn)
    ACCENT_COLOR = (255, 100, 100)        # Coral Red (Hồng Đào)
    DARK_OVERLAY = (0, 0, 0, 200)
    PANEL_COLOR = (139, 0, 0)             # Dark Red Panel
    PANEL_DARK = (100, 0, 0)              # Darker Red
    TEXT_SHADOW = (80, 20, 20)
    COIN_COLOR = (255, 215, 0)            # Gold
    
    # Tet Special Colors
    TET_RED = (200, 30, 30)
    TET_GOLD = (255, 215, 0)
    TET_PINK = (255, 182, 193)            # Hoa Đào
    TET_YELLOW = (255, 223, 0)            # Hoa Mai
    LANTERN_RED = (220, 50, 50)
    LANTERN_GOLD = (255, 200, 50)
    FIREWORK_COLORS = [
        (255, 50, 50),
        (255, 215, 0),
        (255, 100, 200),
        (100, 255, 100),
        (100, 200, 255),
        (255, 150, 50)
    ]
    
    # Gradient colors for Tet night sky
    SKY_TOP = (15, 15, 40)                # Deep night blue
    SKY_BOTTOM = (40, 20, 60)             # Purple night
else:
    # Default Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    SKY_BLUE = (135, 206, 235)
    
    PRIMARY_COLOR = (255, 198, 51)
    SECONDARY_COLOR = (83, 189, 149)
    ACCENT_COLOR = (255, 107, 107)
    DARK_OVERLAY = (0, 0, 0, 180)
    PANEL_COLOR = (222, 184, 135)
    PANEL_DARK = (139, 90, 43)
    TEXT_SHADOW = (50, 50, 50)
    COIN_COLOR = (255, 215, 0)
    
    SKY_TOP = (135, 206, 250)
    SKY_BOTTOM = (176, 224, 230)

# =============================================================================
# DIFFICULTY SETTINGS - Enhanced for Tet
# =============================================================================

DIFFICULTIES = {
    "easy": {
        "gravity": 0.20,
        "jump": -4.5,
        "scroll_speed": 2.5,
        "pipe_gap": 180,
        "pipe_frequency": 2000,
        "coin_frequency": 3000,
        "lixi_frequency": 4000 if TET_MODE else 0
    },
    "medium": {
        "gravity": 0.25,
        "jump": -5,
        "scroll_speed": 3,
        "pipe_gap": 150,
        "pipe_frequency": 1500,
        "coin_frequency": 2500,
        "lixi_frequency": 3000 if TET_MODE else 0
    },
    "hard": {
        "gravity": 0.30,
        "jump": -5.5,
        "scroll_speed": 4,
        "pipe_gap": 120,
        "pipe_frequency": 1200,
        "coin_frequency": 2000,
        "lixi_frequency": 2500 if TET_MODE else 0
    }
}

# Default difficulty
CURRENT_DIFFICULTY = "medium"

# Physics (default)
GRAVITY = 0.25
BIRD_JUMP = -5
SCROLL_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500

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
BIRD_ANIMATION_SPEED = 150

# Pipe Settings
PIPE_WIDTH = 52
PIPE_MIN_HEIGHT = 50

# Coin Settings
COIN_SIZE = 30
COIN_VALUE = 1

# Lì Xì Settings (Tet Special)
LIXI_SIZE = 40
LIXI_VALUES = [5, 10, 20, 50, 88, 168]  # Lucky numbers

# Power-up Settings
POWERUP_SIZE = 35
POWERUP_DURATION = 5000

# Particle Settings
PARTICLE_COUNT = 15
PARTICLE_LIFETIME = 500
FIREWORK_PARTICLE_COUNT = 50 if TET_MODE else 0

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
FADE_SPEED = 8
TRANSITION_SPEED = 15

# Score file
SCORE_FILE = os.path.join(BASE_DIR, "highscore.json")
DATA_FILE = os.path.join(BASE_DIR, "gamedata.json")

# =============================================================================
# SKINS - Enhanced with Tet Edition Skins
# =============================================================================

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
    },
    # =========== TẾT SPECIAL SKINS ===========
    "tet_dragon": {
        "name": "Rồng Vàng 🐉",
        "price": 888,
        "description": "Năm Rồng Thịnh Vượng!",
        "ability": "lixi_magnet",
        "unlocked": False,
        "tet_exclusive": True,
        "colors": {
            "body": (255, 215, 0),
            "accent": (200, 50, 50),
            "eyes": (255, 255, 255)
        }
    },
    "tet_lucky": {
        "name": "Chim Lộc 🧧",
        "price": 168,
        "description": "Lộc đầu năm!",
        "ability": "double_lixi",
        "unlocked": False,
        "tet_exclusive": True,
        "colors": {
            "body": (200, 30, 30),
            "accent": (255, 215, 0),
            "eyes": (255, 255, 255)
        }
    },
    "tet_blossom": {
        "name": "Hoa Đào 🌸",
        "price": 268,
        "description": "Xuân về hoa nở!",
        "ability": "petal_trail",
        "unlocked": False,
        "tet_exclusive": True,
        "colors": {
            "body": (255, 182, 193),
            "accent": (200, 100, 120),
            "eyes": (50, 50, 50)
        }
    },
    "tet_fortune": {
        "name": "Tài Phú 💰",
        "price": 688,
        "description": "Phát Tài Phát Lộc!",
        "ability": "fortune_boost",
        "unlocked": False,
        "tet_exclusive": True,
        "colors": {
            "body": (255, 223, 0),
            "accent": (255, 100, 50),
            "eyes": (50, 50, 50)
        }
    },
    "tet_lantern": {
        "name": "Đèn Lồng 🏮",
        "price": 388,
        "description": "Lung linh đêm hội!",
        "ability": "glow_aura",
        "unlocked": False,
        "tet_exclusive": True,
        "colors": {
            "body": (220, 50, 50),
            "accent": (255, 200, 50),
            "eyes": (255, 255, 200)
        }
    }
}

# =============================================================================
# POWER-UPS - Enhanced with Tet abilities
# =============================================================================

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
    },
    # Tet Special Power-ups
    "lixi_magnet": {
        "name": "Lì Xì Magnet",
        "duration": 10000,
        "color": (255, 50, 50)
    },
    "double_lixi": {
        "name": "2x Lì Xì",
        "duration": 15000,
        "color": (255, 215, 0)
    },
    "firework_burst": {
        "name": "Firework Power",
        "duration": 5000,
        "color": (255, 100, 200)
    }
}

# Combo system
COMBO_THRESHOLD = 3
COMBO_MULTIPLIER = 1.5

# =============================================================================
# TET GREETINGS - Vietnamese New Year Messages
# =============================================================================

TET_GREETINGS = [
    "Chúc Mừng Năm Mới! 🎊",
    "An Khang Thịnh Vượng! 🧧",
    "Vạn Sự Như Ý! ✨",
    "Phát Tài Phát Lộc! 💰",
    "Sức Khỏe Dồi Dào! 💪",
    "Năm Mới Bình An! 🏠",
    "Tấn Tài Tấn Lộc! 🐉",
    "Xuân Về Trăm Hoa Nở! 🌸"
]

TET_DECORATIONS = {
    "lanterns": True,
    "fireworks": True,
    "cherry_blossoms": True,
    "apricot_flowers": True,
    "red_envelopes": True,
    "dragons": True
}
