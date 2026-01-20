import pygame
import math
import os
from settings import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, difficulty="medium", skin_id="default"):
        super().__init__()
        

        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.gravity = diff_settings["gravity"]
        self.jump_power = diff_settings["jump"]
        self.base_gravity = self.gravity
        self.base_jump = self.jump_power
        

        self.skin_id = skin_id
        self.create_sprite()
        

        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        

        self.velocity = 0
        self.angle = 0
        self.target_angle = 0
        

        self.animation_frame = 0
        self.last_animation_time = pygame.time.get_ticks()
        self.animation_speed = BIRD_ANIMATION_SPEED
        

        self.alive = True
        self.has_shield = False
        self.shield_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        

        self.glow_alpha = 0
        self.glow_direction = 5
    
    def create_sprite(self):
        """Create bird sprite programmatically based on skin"""
        self.base_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
        

        skin_colors = self.get_skin_colors()
        body_color = skin_colors["body"]
        body_dark = skin_colors["dark"]
        wing_color = skin_colors["wing"]
        eye_color = skin_colors.get("eye", WHITE)
        beak_color = skin_colors.get("beak", (255, 140, 50))
        
        center_x, center_y = BIRD_WIDTH // 2, BIRD_HEIGHT // 2
        

        pygame.draw.ellipse(self.base_image, body_color, (2, 3, BIRD_WIDTH - 8, BIRD_HEIGHT - 6))
        pygame.draw.ellipse(self.base_image, body_dark, (2, 3, BIRD_WIDTH - 8, BIRD_HEIGHT - 6), 2)
        

        wing_rect = pygame.Rect(6, center_y - 1, 14, 12)
        pygame.draw.ellipse(self.base_image, wing_color, wing_rect)
        

        pygame.draw.circle(self.base_image, eye_color, (center_x + 6, center_y - 4), 7)

        pygame.draw.circle(self.base_image, BLACK, (center_x + 8, center_y - 4), 4)

        pygame.draw.circle(self.base_image, WHITE, (center_x + 6, center_y - 6), 2)
        

        beak_points = [
            (BIRD_WIDTH - 8, center_y),
            (BIRD_WIDTH, center_y + 3),
            (BIRD_WIDTH - 8, center_y + 6)
        ]
        pygame.draw.polygon(self.base_image, beak_color, beak_points)
        

        self.add_skin_effects()
        
        self.image = self.base_image.copy()
        
    def get_skin_colors(self):
        """Get colors for each skin type"""
        colors = {
            "default": {"body": (255, 220, 50), "dark": (255, 180, 30), "wing": (255, 200, 40)},
            "red_angry": {"body": (220, 50, 50), "dark": (180, 30, 30), "wing": (200, 40, 40)},
            "blue_ice": {"body": (150, 220, 255), "dark": (100, 180, 230), "wing": (180, 230, 255)},
            "pink_love": {"body": (255, 150, 180), "dark": (230, 120, 150), "wing": (255, 180, 200)},
            "ninja": {"body": (50, 50, 60), "dark": (30, 30, 40), "wing": (40, 40, 50), "eye": (200, 200, 200)},
            "robot": {"body": (180, 180, 190), "dark": (140, 140, 150), "wing": (160, 160, 170), "eye": (100, 200, 255)},
            "golden": {"body": (255, 215, 0), "dark": (218, 165, 32), "wing": (255, 200, 0)},
            "zombie": {"body": (120, 180, 100), "dark": (90, 140, 80), "wing": (100, 150, 90)},
            "rainbow": {"body": (255, 100, 100), "dark": (200, 80, 80), "wing": (100, 200, 255)},
            "fire": {"body": (255, 120, 50), "dark": (230, 80, 30), "wing": (255, 200, 50)},
            "galaxy": {"body": (100, 50, 150), "dark": (70, 30, 120), "wing": (150, 100, 200)}
        }
        return colors.get(self.skin_id, colors["default"])
        
    def add_skin_effects(self):
        """Add special visual effects for certain skins"""
        center_x, center_y = BIRD_WIDTH // 2, BIRD_HEIGHT // 2
        
        if self.skin_id == "golden":

            crown_points = [(center_x - 8, 2), (center_x - 4, 8), (center_x, 2), 
                          (center_x + 4, 8), (center_x + 8, 2)]
            pygame.draw.polygon(self.base_image, (255, 215, 0), crown_points)
            
        elif self.skin_id == "ninja":

            pygame.draw.line(self.base_image, (200, 50, 50), (5, center_y - 6), (BIRD_WIDTH - 10, center_y - 6), 3)
            
        elif self.skin_id == "robot":

            pygame.draw.line(self.base_image, (100, 100, 100), (center_x, 2), (center_x, 10), 2)
            pygame.draw.circle(self.base_image, (100, 200, 255), (center_x, 2), 3)
            
    def update(self):
        if not self.alive:
            return
        
        now = pygame.time.get_ticks()
        
        if self.has_shield and now > self.shield_timer:
            self.has_shield = False
            
        if self.invincible and now > self.invincible_timer:
            self.invincible = False
        

        self.velocity += self.gravity
        self.rect.y += int(self.velocity)
        

        self.target_angle = -self.velocity * 3
        self.target_angle = max(-90, min(25, self.target_angle))
        

        angle_diff = self.target_angle - self.angle
        self.angle += angle_diff * 0.2
        

        self.image = pygame.transform.rotate(self.base_image, self.angle)
        

        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        

        if self.has_shield or self.invincible:
            self.glow_alpha += self.glow_direction
            if self.glow_alpha >= 100 or self.glow_alpha <= 20:
                self.glow_direction *= -1
        
    def jump(self):
        if self.alive:
            self.velocity = self.jump_power
            
    def die(self):
        self.alive = False
        self.velocity = 0
        
    def activate_shield(self, duration=5000):
        self.has_shield = True
        self.shield_timer = pygame.time.get_ticks() + duration
        
    def activate_invincible(self, duration=3000):
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks() + duration
        
    def is_protected(self):
        return self.has_shield or self.invincible
        
    def draw_effects(self, screen):
        if self.has_shield:
            bubble_surf = pygame.Surface((BIRD_WIDTH + 20, BIRD_HEIGHT + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(bubble_surf, (100, 200, 255, self.glow_alpha), 
                              (0, 0, BIRD_WIDTH + 20, BIRD_HEIGHT + 20), 3)
            screen.blit(bubble_surf, (self.rect.centerx - BIRD_WIDTH // 2 - 10, 
                                       self.rect.centery - BIRD_HEIGHT // 2 - 10))
            
        if self.invincible:
            glow_surf = pygame.Surface((BIRD_WIDTH + 30, BIRD_HEIGHT + 30), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (255, 215, 0, self.glow_alpha), 
                              (0, 0, BIRD_WIDTH + 30, BIRD_HEIGHT + 30))
            screen.blit(glow_surf, (self.rect.centerx - BIRD_WIDTH // 2 - 15, 
                                     self.rect.centery - BIRD_HEIGHT // 2 - 15))
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
