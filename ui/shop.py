import pygame
import os
from settings import *

class ShopMenu:
    """Enhanced skin shop menu with Tet theme and new skins"""
    
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
        
        # Default colors
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
            "galaxy": (100, 50, 150),
            # Tet special skins
            "tet_dragon": (255, 215, 0),
            "tet_lucky": (200, 30, 30),
            "tet_blossom": (255, 182, 193),
            "tet_fortune": (255, 223, 0),
            "tet_lantern": (220, 50, 50)
        }
        
        # Get skin info for custom colors
        skin_info = SKINS.get(skin_id, {})
        if "colors" in skin_info:
            color = skin_info["colors"]["body"]
        else:
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
        beak_color = (255, 140, 50)
        if skin_id.startswith("tet_"):
            beak_color = TET_GOLD if TET_MODE else (255, 200, 50)
        pygame.draw.polygon(surf, beak_color, [(42, 18), (50, 20), (42, 23)])
        
        # Special decorations for Tet skins
        if skin_id == "tet_dragon":
            # Dragon horns
            pygame.draw.polygon(surf, (255, 200, 50), [(15, 4), (18, 0), (21, 4)])
            pygame.draw.polygon(surf, (255, 200, 50), [(8, 6), (10, 2), (14, 5)])
        elif skin_id == "tet_lucky":
            # Red envelope pattern
            pygame.draw.circle(surf, (255, 215, 0), (22, 14), 4)
        elif skin_id == "tet_blossom":
            # Flower petals
            for i in range(5):
                angle = i * 72 * 3.14159 / 180
                px = 10 + int(5 * (1 if i % 2 == 0 else -1))
                pygame.draw.circle(surf, (255, 200, 210), (px, 8), 3)
        elif skin_id == "tet_lantern":
            # Glowing effect
            pygame.draw.circle(surf, (255, 255, 200), (22, 14), 8, 2)
        
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
        
        # Sort to show Tet skins first if in Tet mode
        if TET_MODE:
            tet_skins = [s for s in skin_ids if s.startswith("tet_")]
            regular_skins = [s for s in skin_ids if not s.startswith("tet_")]
            skin_ids = tet_skins + regular_skins
        
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
        # Solid background with Tet styling
        bg_color = (50, 25, 35) if TET_MODE else (40, 44, 52)
        self.screen.fill(bg_color)
        
        # Header with Tet styling
        header_color = PANEL_COLOR if TET_MODE else PANEL_DARK
        pygame.draw.rect(self.screen, header_color, (0, 0, SCREEN_WIDTH, 65))
        
        if TET_MODE:
            pygame.draw.rect(self.screen, TET_GOLD, (0, 62, SCREEN_WIDTH, 3))
        
        # Title
        title_text = "CỬA HÀNG SKIN" if TET_MODE else "SKIN SHOP"
        title = self.title_font.render(title_text, True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 12))
        
        # Coins
        coin_label = "Xu:" if TET_MODE else "Coins:"
        coin_text = f"{coin_label} {self.game_data.coins}"
        coin_surf = self.label_font.render(coin_text, True, COIN_COLOR)
        self.screen.blit(coin_surf, (SCREEN_WIDTH - 110, 22))
        
        # Back button with Tet styling
        back_color = TET_RED if TET_MODE else ACCENT_COLOR
        pygame.draw.rect(self.screen, back_color, self.back_button_rect, border_radius=8)
        if TET_MODE:
            pygame.draw.rect(self.screen, TET_GOLD, self.back_button_rect, 2, border_radius=8)
        
        back_text_str = "VỀ" if TET_MODE else "BACK"
        back_text = self.small_font.render(back_text_str, True, WHITE)
        self.screen.blit(back_text, (self.back_button_rect.centerx - back_text.get_width() // 2,
                                     self.back_button_rect.centery - back_text.get_height() // 2))
        
        # Tet banner if in Tet mode
        if TET_MODE:
            self.draw_tet_banner()
        
        # Skin cards
        self.draw_skin_cards()
        
        # Selected skin panel
        if self.selected_skin:
            self.draw_selected_panel()
    
    def draw_tet_banner(self):
        """Draw Tet promotional banner"""
        banner_rect = pygame.Rect(10, 68, SCREEN_WIDTH - 20, 18)
        pygame.draw.rect(self.screen, TET_RED, banner_rect, border_radius=4)
        
        banner_text = "🧧 Skin Tết 2026 - Giảm giá đặc biệt! 🧧"
        text = self.small_font.render(banner_text, True, TET_GOLD)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))
            
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
            is_tet_exclusive = skin_info.get("tet_exclusive", False)
            
            rect = pygame.Rect(card["rect"].x, adjusted_y, card["rect"].width, card["rect"].height)
            
            # Card background with special styling for Tet skins
            if is_selected:
                color = TET_GOLD if TET_MODE else PRIMARY_COLOR
            elif is_equipped:
                color = SECONDARY_COLOR
            elif is_tet_exclusive:
                color = (80, 30, 40)  # Dark red for Tet skins
            elif is_unlocked:
                color = (100, 100, 110)
            else:
                color = (60, 60, 70)
                
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            
            # Border
            if is_selected:
                border_color = WHITE
            elif is_tet_exclusive:
                border_color = TET_GOLD
            else:
                border_color = None
                
            if border_color:
                pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)
            
            # Tet exclusive badge
            if is_tet_exclusive:
                badge_rect = pygame.Rect(rect.x + 2, rect.y + 2, 25, 14)
                pygame.draw.rect(self.screen, TET_RED, badge_rect, border_radius=4)
                badge_text = self.small_font.render("TẾT", True, WHITE)
                # Scale down the text
                pygame.draw.rect(self.screen, TET_RED, badge_rect, border_radius=4)
            
            # Skin preview (cached)
            if skin_id in ShopMenu._skin_cache:
                preview = ShopMenu._skin_cache[skin_id]
                preview_rect = preview.get_rect(center=(rect.centerx, rect.y + 38))
                self.screen.blit(preview, preview_rect)
            
            # Name
            name = self.small_font.render(skin_info["name"], True, WHITE)
            self.screen.blit(name, (rect.centerx - name.get_width() // 2, rect.y + 70))
            
            # Status
            if is_equipped:
                status_text = "ĐANG DÙNG" if TET_MODE else "EQUIPPED"
                status_color = (150, 255, 150)
            elif is_unlocked:
                status_text = "ĐÃ MUA" if TET_MODE else "OWNED"
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
        is_tet_exclusive = skin_info.get("tet_exclusive", False)
        
        # Bottom panel with Tet styling
        panel_color = PANEL_COLOR if TET_MODE else (222, 184, 135)
        pygame.draw.rect(self.screen, panel_color, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120))
        
        border_color = TET_GOLD if TET_MODE else PANEL_DARK
        pygame.draw.rect(self.screen, border_color, (0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 3))
        
        # Description
        desc = self.label_font.render(skin_info["description"], True, WHITE)
        self.screen.blit(desc, (20, SCREEN_HEIGHT - 110))
        
        # Ability
        if skin_info.get("ability"):
            ability_name = skin_info['ability'].replace('_', ' ').title()
            ability_label = "Kỹ năng:" if TET_MODE else "Ability:"
            ability_text = f"{ability_label} {ability_name}"
            ability = self.small_font.render(ability_text, True, PRIMARY_COLOR)
            self.screen.blit(ability, (20, SCREEN_HEIGHT - 85))
        
        # Tet exclusive note
        if is_tet_exclusive:
            tet_note = self.small_font.render("🧧 Skin độc quyền Tết 2026!", True, TET_GOLD)
            self.screen.blit(tet_note, (20, SCREEN_HEIGHT - 65))
        
        # Button
        if not is_equipped:
            if is_unlocked:
                btn_color = SECONDARY_COLOR
                btn_text = "SỬ DỤNG" if TET_MODE else "EQUIP"
            else:
                can_afford = self.game_data.coins >= skin_info["price"]
                btn_color = (TET_RED if TET_MODE else PRIMARY_COLOR) if can_afford else (100, 100, 100)
                btn_label = "MUA" if TET_MODE else "BUY"
                btn_text = f"{btn_label} {skin_info['price']}"
                
            pygame.draw.rect(self.screen, btn_color, self.action_button_rect, border_radius=8)
            if TET_MODE:
                pygame.draw.rect(self.screen, TET_GOLD, self.action_button_rect, 2, border_radius=8)
            
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
