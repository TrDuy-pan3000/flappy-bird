import pygame
import os
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, color=PRIMARY_COLOR, hover_color=None, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.base_color = color
        self.hover_color = hover_color or tuple(min(255, c + 30) for c in color)
        self.text_color = text_color
        self.is_hovered = False
        self.font = get_vn_font(FONT_MEDIUM)
        

        self.scale = 1.0
        self.target_scale = 1.0
        
    def update(self, mouse_pos):
        """Update button state"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.05 if self.is_hovered else 1.0
        

        self.scale += (self.target_scale - self.scale) * 0.2
        
    def draw(self, screen):
        """Draw the button with modern styling"""

        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        

        shadow_rect = scaled_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 80), shadow_rect, border_radius=BUTTON_RADIUS)
        

        color = self.hover_color if self.is_hovered else self.base_color
        pygame.draw.rect(screen, color, scaled_rect, border_radius=BUTTON_RADIUS)
        

        border_color = tuple(max(0, c - 40) for c in color)
        pygame.draw.rect(screen, border_color, scaled_rect, 3, border_radius=BUTTON_RADIUS)
        

        highlight_rect = pygame.Rect(scaled_rect.x + 4, scaled_rect.y + 4, scaled_rect.width - 8, 8)
        highlight_color = tuple(min(255, c + 60) for c in color)
        pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=4)
        

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        

        shadow_surf = self.font.render(self.text, True, TEXT_SHADOW)
        screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text_surf, text_rect)
        
    def is_clicked(self, event):
        """Check if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class Panel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        """Draw a wooden panel background"""

        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=12)
        

        pygame.draw.rect(screen, PANEL_COLOR, self.rect, border_radius=12)
        

        pygame.draw.rect(screen, PANEL_DARK, self.rect, 4, border_radius=12)
        

        inner = self.rect.inflate(-8, -8)
        pygame.draw.rect(screen, tuple(min(255, c + 20) for c in PANEL_COLOR), inner, border_radius=8)


class MedalDisplay:
    def __init__(self, x, y, size=64):
        self.x = x
        self.y = y
        self.size = size
        self.medal_type = None
        self.images = {}
        self.load_images()
        
    def load_images(self):
        """Load medal images"""
        medal_types = ["bronze", "silver", "gold", "platinum"]
        
        for medal in medal_types:
            path = os.path.join(ASSETS_DIR, f"medal_{medal}.png")
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    self.images[medal] = pygame.transform.scale(img, (self.size, self.size))
                except pygame.error:
                    self.images[medal] = self.create_fallback(medal)
            else:
                self.images[medal] = self.create_fallback(medal)
        
    def create_fallback(self, medal_type):
        """Create fallback medal graphics"""
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        colors = {
            "bronze": (205, 127, 50),
            "silver": (192, 192, 192),
            "gold": (255, 215, 0),
            "platinum": (229, 228, 226)
        }
        
        color = colors.get(medal_type, (255, 215, 0))
        center = self.size // 2
        

        pygame.draw.circle(surf, color, (center, center), center - 4)
        pygame.draw.circle(surf, tuple(max(0, c - 40) for c in color), (center, center), center - 4, 3)
        

        star_points = []
        for i in range(5):
            outer_angle = -90 + i * 72
            inner_angle = outer_angle + 36
            
            ox = center + int((center - 12) * 0.7 * pygame.math.Vector2(1, 0).rotate(outer_angle).x)
            oy = center + int((center - 12) * 0.7 * pygame.math.Vector2(1, 0).rotate(outer_angle).y)
            
            ix = center + int((center - 12) * 0.3 * pygame.math.Vector2(1, 0).rotate(inner_angle).x)
            iy = center + int((center - 12) * 0.3 * pygame.math.Vector2(1, 0).rotate(inner_angle).y)
            
            star_points.extend([(ox, oy), (ix, iy)])
            
        if len(star_points) >= 3:
            pygame.draw.polygon(surf, tuple(max(0, c - 20) for c in color), star_points)
            
        return surf
        
    def set_medal(self, medal_type):
        self.medal_type = medal_type
        
    def draw(self, screen):
        if self.medal_type and self.medal_type in self.images:
            screen.blit(self.images[self.medal_type], (self.x, self.y))


class ScoreDisplay:
    def __init__(self, x, y, font_size=FONT_LARGE):
        self.x = x
        self.y = y
        self.font = get_vn_font(font_size)
        self.score = 0
        
    def set_score(self, score):
        self.score = score
        
    def draw(self, screen, center=True):
        """Draw score with shadow effect"""
        text = str(self.score)
        

        shadow_surf = self.font.render(text, True, TEXT_SHADOW)
        text_surf = self.font.render(text, True, WHITE)
        
        if center:
            shadow_rect = shadow_surf.get_rect(center=(self.x + 2, self.y + 2))
            text_rect = text_surf.get_rect(center=(self.x, self.y))
        else:
            shadow_rect = shadow_surf.get_rect(topleft=(self.x + 2, self.y + 2))
            text_rect = text_surf.get_rect(topleft=(self.x, self.y))
            
        screen.blit(shadow_surf, shadow_rect)
        screen.blit(text_surf, text_rect)
