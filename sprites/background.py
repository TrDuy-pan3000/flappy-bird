import pygame
from settings import *

class Background:
    """Optimized background with cached surface"""
    
    _cached_surface = None
    
    def __init__(self, difficulty="medium"):
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"] * 0.3
        self.x = 0
        
        # Create cached background if not exists
        if Background._cached_surface is None:
            Background._cached_surface = self.create_background()
        
        self.image = Background._cached_surface
        
    def create_background(self):
        """Create beautiful sky background"""
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Sky gradient
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            ratio = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(135 + (176 - 135) * ratio)
            g = int(206 + (224 - 206) * ratio)
            b = int(250 + (230 - 250) * ratio)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Clouds
        cloud_data = [(40, 50), (150, 80), (280, 40), (60, 150), (220, 170), (350, 100)]
        for cx, cy in cloud_data:
            # Cloud made of circles
            pygame.draw.circle(surf, (255, 255, 255), (cx, cy), 25)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 20, cy - 5), 20)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 35, cy), 22)
            pygame.draw.circle(surf, (255, 255, 255), (cx - 15, cy + 5), 18)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 15, cy + 8), 20)
        
        # City silhouette
        city_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        city_color = (120, 130, 160)
        
        buildings = [
            (0, 40), (25, 55), (50, 35), (75, 70), (100, 50),
            (125, 60), (150, 45), (175, 80), (200, 55), (225, 65),
            (250, 50), (275, 40), (300, 75), (325, 55), (350, 60), (375, 45)
        ]
        
        for x, h in buildings:
            pygame.draw.rect(surf, city_color, (x, city_y - h + 40, 22, h))
            # Windows
            for wy in range(city_y - h + 45, city_y + 35, 8):
                for wx in range(x + 3, x + 19, 6):
                    pygame.draw.rect(surf, (180, 180, 150), (wx, wy, 3, 4))
        
        return surf
            
    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -SCREEN_WIDTH:
            self.x = 0
            
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), 0))
        screen.blit(self.image, (int(self.x) + SCREEN_WIDTH, 0))


class Ground(pygame.sprite.Sprite):
    """Optimized ground with cached surface"""
    
    _cached_surface = None
    
    def __init__(self, difficulty="medium"):
        super().__init__()
        
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"]
        self.x = 0
        
        if Ground._cached_surface is None:
            Ground._cached_surface = self.create_ground()
            
        self.image = Ground._cached_surface
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        
    def create_ground(self):
        """Create ground surface"""
        surf = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Grass
        pygame.draw.rect(surf, (100, 180, 80), (0, 0, SCREEN_WIDTH, 18))
        
        # Grass blades
        for x in range(0, SCREEN_WIDTH, 5):
            pygame.draw.line(surf, (80, 160, 60), (x, 18), (x + 2, 0), 2)
        
        # Dirt
        pygame.draw.rect(surf, (139, 90, 43), (0, 18, SCREEN_WIDTH, GROUND_HEIGHT - 18))
        
        # Texture
        import random
        random.seed(42)
        for _ in range(40):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(22, GROUND_HEIGHT - 5)
            pygame.draw.circle(surf, (160, 110, 60), (x, y), 2)
            
        return surf
                
    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -SCREEN_WIDTH:
            self.x = 0
            
    def draw(self, screen):
        y = SCREEN_HEIGHT - GROUND_HEIGHT
        screen.blit(self.image, (int(self.x), y))
        screen.blit(self.image, (int(self.x) + SCREEN_WIDTH, y))
