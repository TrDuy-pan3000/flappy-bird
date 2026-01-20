import json
import os
from settings import SCORE_FILE, DATA_FILE, MEDAL_THRESHOLDS, SKINS

class ScoreManager:
    def __init__(self):
        self.high_scores = {
            "easy": 0,
            "medium": 0,
            "hard": 0
        }
        self.current_score = 0
        self.is_new_high_score = False
        self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    self.high_scores = data.get("high_scores", self.high_scores)
        except (json.JSONDecodeError, IOError):
            pass
    
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(SCORE_FILE, 'w') as f:
                json.dump({"high_scores": self.high_scores}, f, indent=2)
        except IOError:
            pass
    
    def update_score(self, score, difficulty="medium"):
        """Update current score and check for new high score"""
        self.current_score = score
        if score > self.high_scores.get(difficulty, 0):
            self.high_scores[difficulty] = score
            self.is_new_high_score = True
            self.save_scores()
            return True
        return False
    
    def get_high_score(self, difficulty="medium"):
        return self.high_scores.get(difficulty, 0)
    
    def reset_current_score(self):
        self.current_score = 0
        self.is_new_high_score = False
    
    def increment_score(self, amount=1):
        self.current_score += amount
        return self.current_score
    
    def get_medal(self, score=None):
        if score is None:
            score = self.current_score
        
        if score >= MEDAL_THRESHOLDS["platinum"]:
            return "platinum"
        elif score >= MEDAL_THRESHOLDS["gold"]:
            return "gold"
        elif score >= MEDAL_THRESHOLDS["silver"]:
            return "silver"
        elif score >= MEDAL_THRESHOLDS["bronze"]:
            return "bronze"
        return None


class GameDataManager:
    """Manages persistent game data like coins and unlocked skins"""
    
    def __init__(self):
        self.coins = 0
        self.current_skin = "default"
        self.unlocked_skins = ["default"]
        self.total_games = 0
        self.total_score = 0
        self.load_data()
    
    def load_data(self):
        """Load game data from file"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.coins = data.get("coins", 0)
                    self.current_skin = data.get("current_skin", "default")
                    self.unlocked_skins = data.get("unlocked_skins", ["default"])
                    self.total_games = data.get("total_games", 0)
                    self.total_score = data.get("total_score", 0)
        except (json.JSONDecodeError, IOError):
            pass
    
    def save_data(self):
        """Save game data to file"""
        try:
            data = {
                "coins": self.coins,
                "current_skin": self.current_skin,
                "unlocked_skins": self.unlocked_skins,
                "total_games": self.total_games,
                "total_score": self.total_score
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass
    
    def add_coins(self, amount):
        """Add coins to wallet"""
        self.coins += amount
        self.save_data()
        return self.coins
    
    def spend_coins(self, amount):
        """Spend coins, returns True if successful"""
        if self.coins >= amount:
            self.coins -= amount
            self.save_data()
            return True
        return False
    
    def unlock_skin(self, skin_id):
        """Unlock a skin"""
        if skin_id not in self.unlocked_skins:
            skin = SKINS.get(skin_id)
            if skin and self.spend_coins(skin["price"]):
                self.unlocked_skins.append(skin_id)
                self.save_data()
                return True
        return False
    
    def is_skin_unlocked(self, skin_id):
        """Check if skin is unlocked"""
        return skin_id in self.unlocked_skins
    
    def set_current_skin(self, skin_id):
        """Set current active skin"""
        if skin_id in self.unlocked_skins:
            self.current_skin = skin_id
            self.save_data()
            return True
        return False
    
    def record_game(self, score):
        """Record game statistics"""
        self.total_games += 1
        self.total_score += score
        self.save_data()
