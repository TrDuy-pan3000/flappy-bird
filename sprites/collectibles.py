import pygame
import os
import random
import math
from settings import *

class Coin(pygame.sprite.Sprite):
    """Collectible coin - optimized with cached sprite"""
    

    _cached_sprite = None
    
    def __init__(self, x, y, difficulty="medium"):
        super().__init__()
        
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"]
        

        if Coin._cached_sprite is None:
            Coin._cached_sprite = self.create_sprite()
        
        self.image = Coin._cached_sprite
        self.rect = self.image.get_rect(center=(x, y))
        

        self.base_y = y
        self.animation_offset = random.uniform(0, math.pi * 2)
        self.collected = False
        

        self.attracted = False
        self.attract_target = None
    
    @staticmethod
    def create_sprite():
        """Create coin sprite"""
        surf = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        
        center = COIN_SIZE // 2
        

        pygame.draw.circle(surf, (255, 200, 0), (center, center), center - 2)
        pygame.draw.circle(surf, (218, 165, 32), (center, center), center - 2, 2)
        

        pygame.draw.circle(surf, (255, 220, 50), (center, center), center - 5)
        

        star_size = center - 8
        for i in range(5):
            angle = -90 + i * 72
            x = center + int(star_size * 0.6 * math.cos(math.radians(angle)))
            y = center + int(star_size * 0.6 * math.sin(math.radians(angle)))
            pygame.draw.circle(surf, (255, 180, 0), (x, y), 2)
            

        pygame.draw.circle(surf, (255, 255, 200), (center - 4, center - 4), 3)
        
        return surf
        
    def update(self):
        if self.collected:
            return
            
        if not self.attracted:
            self.rect.x -= self.scroll_speed
        else:
            if self.attract_target:
                dx = self.attract_target.rect.centerx - self.rect.centerx
                dy = self.attract_target.rect.centery - self.rect.centery
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    self.rect.x += int(dx / dist * 8)
                    self.rect.y += int(dy / dist * 8)
        

        time = pygame.time.get_ticks() / 200 + self.animation_offset
        self.rect.centery = int(self.base_y + math.sin(time) * 5)
        
        if self.rect.right < 0:
            self.kill()
            
    def attract_to(self, bird):
        self.attracted = True
        self.attract_target = bird


class PowerUp(pygame.sprite.Sprite):
    """Collectible power-up - optimized with cached sprites"""
    

    _cached_sprites = {}
    
    def __init__(self, x, y, power_type, difficulty="medium"):
        super().__init__()
        
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"]
        
        self.power_type = power_type
        

        if power_type not in PowerUp._cached_sprites:
            PowerUp._cached_sprites[power_type] = self.create_sprite()
        
        self.image = PowerUp._cached_sprites[power_type]
        self.rect = self.image.get_rect(center=(x, y))
        
        self.base_y = y
        
    def create_sprite(self):
        """Create power-up sprite"""
        surf = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE), pygame.SRCALPHA)
        
        power_info = POWERUPS.get(self.power_type, {"color": (200, 200, 200)})
        color = power_info["color"]
        
        center = POWERUP_SIZE // 2
        

        pygame.draw.circle(surf, (*color, 80), (center, center), center)
        

        pygame.draw.circle(surf, color, (center, center), center - 4)
        pygame.draw.circle(surf, tuple(max(0, c - 40) for c in color), (center, center), center - 4, 2)
        

        if self.power_type == "shield":

            pygame.draw.arc(surf, WHITE, (8, 6, POWERUP_SIZE - 16, POWERUP_SIZE - 12), 0, math.pi, 3)
            pygame.draw.line(surf, WHITE, (8, center), (POWERUP_SIZE - 8, center), 2)
            

            pygame.draw.arc(surf, WHITE, (10, 8, POWERUP_SIZE - 20, POWERUP_SIZE - 16), 
                           math.pi, 2 * math.pi, 3)
            pygame.draw.line(surf, WHITE, (10, center), (10, center + 8), 3)
            pygame.draw.line(surf, WHITE, (POWERUP_SIZE - 10, center), 
                           (POWERUP_SIZE - 10, center + 8), 3)
            

            pygame.draw.polygon(surf, WHITE, [
                (center, 8), (center - 7, center), (center, POWERUP_SIZE - 8), (center + 7, center)
            ], 2)
            

            font = pygame.font.Font(None, 18)
            text = font.render("2x", True, WHITE)
            text_rect = text.get_rect(center=(center, center))
            surf.blit(text, text_rect)
        
        return surf
        
    def update(self):
        self.rect.x -= self.scroll_speed
        
        time = pygame.time.get_ticks() / 200
        self.rect.centery = int(self.base_y + math.sin(time) * 8)
        
        if self.rect.right < 0:
            self.kill()
