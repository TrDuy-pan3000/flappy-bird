import pygame
import os
from settings import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, is_top=False, difficulty="medium"):
        super().__init__()
        
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"]
        
        self.is_top = is_top
        self.scored = False
        
        # Calculate height
        if is_top:
            pipe_height = position[1]
        else:
            pipe_height = SCREEN_HEIGHT - position[1]
        
        pipe_height = max(pipe_height, 50)
        
        # Create sprite programmatically (more reliable than loading images)
        self.create_sprite(pipe_height)
        
        self.rect = self.image.get_rect()
        
        if self.is_top:
            self.rect.bottomleft = position
        else:
            self.rect.topleft = position
            
    def create_sprite(self, height):
        """Create pipe sprite programmatically"""
        self.image = pygame.Surface((PIPE_WIDTH, height), pygame.SRCALPHA)
        
        # Colors
        body_color = (46, 204, 113)      # Green
        dark_color = (39, 174, 96)       # Dark green
        highlight = (88, 214, 141)       # Light green
        border_color = (30, 100, 60)     # Border
        
        # Main body
        pygame.draw.rect(self.image, body_color, (4, 0, PIPE_WIDTH - 8, height))
        
        # Left highlight
        pygame.draw.rect(self.image, highlight, (4, 0, 10, height))
        
        # Right shadow
        pygame.draw.rect(self.image, dark_color, (PIPE_WIDTH - 14, 0, 10, height))
        
        # Cap
        cap_height = 28
        cap_extra = 4  # How much cap extends beyond body
        
        if self.is_top:
            # Cap at bottom
            cap_y = height - cap_height
            pygame.draw.rect(self.image, body_color, (-cap_extra, cap_y, PIPE_WIDTH + cap_extra * 2, cap_height))
            pygame.draw.rect(self.image, highlight, (-cap_extra, cap_y, PIPE_WIDTH + cap_extra * 2, 4))
            pygame.draw.rect(self.image, dark_color, (-cap_extra, cap_y + cap_height - 4, PIPE_WIDTH + cap_extra * 2, 4))
            pygame.draw.rect(self.image, border_color, (-cap_extra, cap_y, PIPE_WIDTH + cap_extra * 2, cap_height), 2)
        else:
            # Cap at top
            pygame.draw.rect(self.image, body_color, (-cap_extra, 0, PIPE_WIDTH + cap_extra * 2, cap_height))
            pygame.draw.rect(self.image, highlight, (-cap_extra, 0, PIPE_WIDTH + cap_extra * 2, 4))
            pygame.draw.rect(self.image, dark_color, (-cap_extra, cap_height - 4, PIPE_WIDTH + cap_extra * 2, 4))
            pygame.draw.rect(self.image, border_color, (-cap_extra, 0, PIPE_WIDTH + cap_extra * 2, cap_height), 2)
        
        # Body border
        pygame.draw.rect(self.image, border_color, (2, 0, PIPE_WIDTH - 4, height), 2)
            
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()
            
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
