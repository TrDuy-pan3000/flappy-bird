import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    """Projectile for combat modes"""
    
    def __init__(self, x, y, direction=1, speed=8, color=(255, 255, 100), owner="player"):
        super().__init__()
        
        self.direction = direction
        self.speed = speed
        self.owner = owner
        

        self.image = pygame.Surface((12, 6), pygame.SRCALPHA)
        

        pygame.draw.ellipse(self.image, color, (0, 0, 12, 6))
        pygame.draw.ellipse(self.image, (255, 255, 255), (2, 1, 4, 3))
        
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.rect.x += self.speed * self.direction
        

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class Laser(pygame.sprite.Sprite):
    """Horizontal laser beam"""
    
    def __init__(self, y, direction=1, speed=0, width=SCREEN_WIDTH):
        super().__init__()
        
        self.warning_time = 1000
        self.active_time = 500
        self.start_time = pygame.time.get_ticks()
        self.is_active = False
        self.is_warning = True
        

        self.image = pygame.Surface((width, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 50, 50, 100), (0, 0, width, 4))
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = 0
        
        self.y = y
        self.width = width
        
    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        
        if elapsed < self.warning_time:

            alpha = 100 + int(math.sin(elapsed / 50) * 50)
            self.image.fill((0, 0, 0, 0))
            pygame.draw.rect(self.image, (255, 50, 50, alpha), (0, 0, self.width, 4))
            
        elif elapsed < self.warning_time + self.active_time:

            if not self.is_active:
                self.is_active = True
                self.is_warning = False
                self.image = pygame.Surface((self.width, 20), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255, 100, 100), (0, 0, self.width, 20))
                pygame.draw.rect(self.image, (255, 255, 200), (0, 8, self.width, 4))
                self.rect = self.image.get_rect()
                self.rect.y = self.y - 8
                self.rect.x = 0
        else:
            self.kill()


class FallingObstacle(pygame.sprite.Sprite):
    """Falling obstacle for Dodge Master"""
    
    def __init__(self, x, obstacle_type="rock", speed=4):
        super().__init__()
        
        self.obstacle_type = obstacle_type
        self.speed = speed
        self.create_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = 0
        
    def create_sprite(self):
        if self.obstacle_type == "rock":
            size = 35
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)

            pygame.draw.polygon(self.image, (120, 120, 130), [
                (size//2, 0), (size, size//2), (size-5, size), 
                (5, size), (0, size//2)
            ])
            pygame.draw.polygon(self.image, (90, 90, 100), [
                (size//2, 0), (size, size//2), (size-5, size), 
                (5, size), (0, size//2)
            ], 2)
            
        elif self.obstacle_type == "missile":
            self.image = pygame.Surface((40, 15), pygame.SRCALPHA)

            pygame.draw.rect(self.image, (200, 50, 50), (5, 3, 30, 9))
            pygame.draw.polygon(self.image, (220, 70, 70), [(35, 3), (40, 7), (35, 12)])

            pygame.draw.polygon(self.image, (150, 40, 40), [(5, 0), (10, 3), (5, 7)])
            pygame.draw.polygon(self.image, (150, 40, 40), [(5, 15), (10, 12), (5, 8)])
            
        elif self.obstacle_type == "bomb":
            size = 30
            self.image = pygame.Surface((size, size + 10), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (40, 40, 45), (size//2, size//2 + 5), size//2)
            pygame.draw.circle(self.image, (60, 60, 65), (size//2, size//2 + 5), size//2, 2)

            pygame.draw.line(self.image, (100, 80, 50), (size//2, 5), (size//2, 0), 3)
            pygame.draw.circle(self.image, (255, 150, 50), (size//2, 0), 4)
            
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class BombFragment(pygame.sprite.Sprite):
    """Fragment from exploded bomb"""
    
    def __init__(self, x, y, angle, speed=6):
        super().__init__()
        
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (80, 80, 85), (4, 4), 4)
        
        self.rect = self.image.get_rect(center=(x, y))
        
        self.vx = math.cos(math.radians(angle)) * speed
        self.vy = math.sin(math.radians(angle)) * speed
        self.lifetime = 60
        
    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)
        self.vy += 0.2
        
        self.lifetime -= 1
        if self.lifetime <= 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class ColorGate(pygame.sprite.Sprite):
    """Colored gate for Memory Flight"""
    
    COLORS = {
        "red": (255, 80, 80),
        "blue": (80, 150, 255),
        "yellow": (255, 220, 80),
        "purple": (180, 100, 255),
        "orange": (255, 150, 80)
    }
    
    def __init__(self, x, color_name, gate_height=100):
        super().__init__()
        
        self.color_name = color_name
        self.base_color = self.COLORS.get(color_name, (200, 200, 200))
        self.gate_height = gate_height
        self.is_highlighted = False
        self.is_correct = None  # None, True, False
        
        self.create_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT // 2
        
    def create_sprite(self):
        width = 60
        self.image = pygame.Surface((width, self.gate_height), pygame.SRCALPHA)
        
        color = self.base_color
        if self.is_highlighted:
            color = tuple(min(255, c + 50) for c in self.base_color)
        

        pygame.draw.rect(self.image, color, (0, 0, width, self.gate_height), border_radius=10)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, width, self.gate_height), 3, border_radius=10)
        

        if self.is_highlighted:
            inner_rect = pygame.Rect(5, 5, width - 10, self.gate_height - 10)
            pygame.draw.rect(self.image, (255, 255, 255, 100), inner_rect, border_radius=8)
            

        if self.is_correct is True:
            pygame.draw.circle(self.image, (100, 255, 100), (width // 2, 20), 10)
        elif self.is_correct is False:
            pygame.draw.line(self.image, (255, 100, 100), (width//2 - 8, 12), (width//2 + 8, 28), 3)
            pygame.draw.line(self.image, (255, 100, 100), (width//2 + 8, 12), (width//2 - 8, 28), 3)
            
    def highlight(self, on=True):
        self.is_highlighted = on
        self.create_sprite()
        
    def set_feedback(self, correct):
        self.is_correct = correct
        self.create_sprite()
        
    def reset(self):
        self.is_highlighted = False
        self.is_correct = None
        self.create_sprite()
