import pygame
import os
from settings import *

class ShopMenu:
    """Optimized skin shop menu with image caching"""
    
    # Class-level image cache
    _skin_cache = {}
    _initialized = False
    
    def __init__(self, screen, game_data):
        self.screen = screen
        self.game_data = game_data
        
        # Fonts (cached)
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Selected skin
        self.selected_skin = None
        
        # Pre-generate all skin previews
        if not ShopMenu._initialized:
            self.preload_skins()
            ShopMenu._initialized = True
        
        # Skin cards - pre-calculated positions
        self.skin_cards = self.setup_cards()
        
        # Button rects
        self.back_button_rect = pygame.Rect(20, 20, 80, 40)
        self.action_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 80, 120, 45)
        
    def preload_skins(self):
        """Pre-generate all skin preview images"""
        for skin_id in SKINS.keys():
            ShopMenu._skin_cache[skin_id] = self.create_skin_preview(skin_id)
            
    def create_skin_preview(self, skin_id):
        """Create a skin preview programmatically"""
        surf = pygame.Surface((50, 38), pygame.SRCALPHA)
        
        colors = {
            "default": (255, 220, 50),
            "red_angry": (220, 50, 50),
            "blue_ice": (150, 220, 255),
            "pink_love": (255, 150, 180),
            "ninja": (50, 50, 60),
            "robot": (180, 180, 190),
            "golden": (255, 215, 0),
            "zombie": (120, 180, 100),
            "rainbow": (255, 100, 100),
            "fire": (255, 120, 50),
            "galaxy": (100, 50, 150)
        }
        
        color = colors.get(skin_id, (255, 220, 50))
        dark = tuple(max(0, c - 40) for c in color)
        
        # Body
        pygame.draw.ellipse(surf, color, (2, 4, 42, 30))
        pygame.draw.ellipse(surf, dark, (2, 4, 42, 30), 2)
        
        # Wing
        pygame.draw.ellipse(surf, dark, (6, 14, 12, 10))
        
        # Eye
        pygame.draw.circle(surf, WHITE, (32, 14), 6)
        pygame.draw.circle(surf, BLACK, (34, 14), 3)
        
        # Beak
        pygame.draw.polygon(surf, (255, 140, 50), [(42, 18), (50, 20), (42, 23)])
        
        return surf
        
    def setup_cards(self):
        """Setup skin card positions"""
        cards = []
        card_width = 100
        card_height = 120
        cards_per_row = 3
        padding = 15
        start_y = 90
        
        skin_ids = list(SKINS.keys())
        
        for i, skin_id in enumerate(skin_ids):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = padding + col * (card_width + padding)
            y = start_y + row * (card_height + padding)
            
            cards.append({
                "id": skin_id,
                "rect": pygame.Rect(x, y, card_width, card_height),
                "skin": SKINS[skin_id]
            })
        
        total_rows = (len(skin_ids) + cards_per_row - 1) // cards_per_row
        total_height = start_y + total_rows * (card_height + padding)
        self.max_scroll = max(0, total_height - SCREEN_HEIGHT + 150)
        
        return cards
        
    def update(self, mouse_pos):
        pass  # No animations needed
        
    def draw(self, background, ground):
        # Solid background for better performance
        self.screen.fill((40, 44, 52))
        
        # Header
        pygame.draw.rect(self.screen, PANEL_DARK, (0, 0, SCREEN_WIDTH, 65))
        
        # Title
        title = self.title_font.render("SKIN SHOP", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 12))
        
        # Coins
        coin_text = f"Coins: {self.game_data.coins}"
        coin_surf = self.label_font.render(coin_text, True, COIN_COLOR)
        self.screen.blit(coin_surf, (SCREEN_WIDTH - 110, 22))
        
        # Back button
        pygame.draw.rect(self.screen, ACCENT_COLOR, self.back_button_rect, border_radius=8)
        back_text = self.small_font.render("BACK", True, WHITE)
        self.screen.blit(back_text, (self.back_button_rect.centerx - back_text.get_width() // 2,
                                     self.back_button_rect.centery - back_text.get_height() // 2))
        
        # Skin cards
        self.draw_skin_cards()
        
        # Selected skin panel
        if self.selected_skin:
            self.draw_selected_panel()
            
    def draw_skin_cards(self):
        """Draw all skin cards"""
        for card in self.skin_cards:
            adjusted_y = card["rect"].y - self.scroll_offset
            
            # Skip if off screen
            if adjusted_y + card["rect"].height < 65 or adjusted_y > SCREEN_HEIGHT - 130:
                continue
            
            skin_id = card["id"]
            skin_info = card["skin"]
            is_unlocked = self.game_data.is_skin_unlocked(skin_id)
            is_equipped = self.game_data.current_skin == skin_id
            is_selected = self.selected_skin == skin_id
            
            rect = pygame.Rect(card["rect"].x, adjusted_y, card["rect"].width, card["rect"].height)
            
            # Card background
            if is_selected:
                color = PRIMARY_COLOR
            elif is_equipped:
                color = SECONDARY_COLOR
            elif is_unlocked:
                color = (100, 100, 110)
            else:
                color = (60, 60, 70)
                
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            
            if is_selected:
                pygame.draw.rect(self.screen, WHITE, rect, 3, border_radius=10)
            
            # Skin preview (cached)
            if skin_id in ShopMenu._skin_cache:
                preview = ShopMenu._skin_cache[skin_id]
                preview_rect = preview.get_rect(center=(rect.centerx, rect.y + 35))
                self.screen.blit(preview, preview_rect)
            
            # Name
            name = self.small_font.render(skin_info["name"], True, WHITE)
            self.screen.blit(name, (rect.centerx - name.get_width() // 2, rect.y + 70))
            
            # Status
            if is_equipped:
                status_text = "EQUIPPED"
                status_color = (150, 255, 150)
            elif is_unlocked:
                status_text = "OWNED"
                status_color = (200, 200, 255)
            else:
                status_text = f"{skin_info['price']}"
                status_color = COIN_COLOR
                
            status = self.small_font.render(status_text, True, status_color)
            self.screen.blit(status, (rect.centerx - status.get_width() // 2, rect.y + 92))
                
    def draw_selected_panel(self):
        """Draw panel for selected skin"""
        skin_info = SKINS.get(self.selected_skin)
        if not skin_info:
            return
            
        is_unlocked = self.game_data.is_skin_unlocked(self.selected_skin)
        is_equipped = self.game_data.current_skin == self.selected_skin
        
        # Bottom panel
        pygame.draw.rect(self.screen, PANEL_COLOR, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))
        pygame.draw.rect(self.screen, PANEL_DARK, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 3))
        
        # Description
        desc = self.label_font.render(skin_info["description"], True, WHITE)
        self.screen.blit(desc, (20, SCREEN_HEIGHT - 110))
        
        # Ability
        if skin_info.get("ability"):
            ability_text = f"Ability: {skin_info['ability'].replace('_', ' ').title()}"
            ability = self.small_font.render(ability_text, True, PRIMARY_COLOR)
            self.screen.blit(ability, (20, SCREEN_HEIGHT - 85))
        
        # Button
        if not is_equipped:
            if is_unlocked:
                btn_color = SECONDARY_COLOR
                btn_text = "EQUIP"
            else:
                can_afford = self.game_data.coins >= skin_info["price"]
                btn_color = PRIMARY_COLOR if can_afford else (100, 100, 100)
                btn_text = f"BUY {skin_info['price']}"
                
            pygame.draw.rect(self.screen, btn_color, self.action_button_rect, border_radius=8)
            text = self.label_font.render(btn_text, True, WHITE)
            self.screen.blit(text, (self.action_button_rect.centerx - text.get_width() // 2,
                                    self.action_button_rect.centery - text.get_height() // 2))
            
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if self.back_button_rect.collidepoint(pos):
                return ("back", None)
            
            # Check cards
            for card in self.skin_cards:
                adjusted_y = card["rect"].y - self.scroll_offset
                rect = pygame.Rect(card["rect"].x, adjusted_y, card["rect"].width, card["rect"].height)
                
                if rect.collidepoint(pos):
                    self.selected_skin = card["id"]
                    return None
            
            # Check action button
            if self.selected_skin and self.action_button_rect.collidepoint(pos):
                is_unlocked = self.game_data.is_skin_unlocked(self.selected_skin)
                is_equipped = self.game_data.current_skin == self.selected_skin
                
                if not is_equipped:
                    if is_unlocked:
                        self.game_data.set_current_skin(self.selected_skin)
                        return ("equipped", self.selected_skin)
                    else:
                        if self.game_data.unlock_skin(self.selected_skin):
                            return ("bought", self.selected_skin)
        
        # Scroll
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 40
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return ("back", None)
                
        return None
