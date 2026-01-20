import pygame
import math
from settings import *

class MiniGameMenu:
    """Enhanced game mode selection menu with hover, scroll, and confirmation"""
    
    def __init__(self, screen):
        self.screen = screen
        
        # Fonts
        self.title_font = pygame.font.Font(None, 42)
        self.label_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.desc_font = pygame.font.Font(None, 18)
        
        # Scrolling
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_velocity = 0
        self.is_dragging = False
        self.drag_start_y = 0
        
        # Hover
        self.hovered_mode = None
        self.hover_scale = {}
        
        # Confirmation dialog
        self.show_confirm = False
        self.confirm_mode = None
        
        # All game modes with detailed info
        self.modes = [
            {
                "id": "classic",
                "name": "Classic Mode",
                "desc": "The original Flappy Bird experience",
                "details": "Fly through pipes endlessly. Simple and addictive!",
                "icon_color": SECONDARY_COLOR,
                "difficulty": "Easy",
            },
            {
                "id": "time_attack",
                "name": "Time Attack",
                "desc": "Score as much as possible in 60 seconds!",
                "details": "Race against time. Every second counts!",
                "icon_color": PRIMARY_COLOR,
                "difficulty": "Medium",
            },
            {
                "id": "zen",
                "name": "Zen Mode", 
                "desc": "Relaxing flight - no obstacles",
                "details": "Just collect coins and enjoy the flight.",
                "icon_color": (150, 200, 255),
                "difficulty": "Easy",
            },
            {
                "id": "bird_battle",
                "name": "Bird Battle",
                "desc": "Epic PvP combat against AI!",
                "details": "Shoot, dodge, use power-ups. Last bird standing wins!",
                "icon_color": ACCENT_COLOR,
                "difficulty": "Hard",
            },
            {
                "id": "dodge_master",
                "name": "Dodge Master",
                "desc": "Survive waves of falling obstacles!",
                "details": "Test your reflexes. How long can you survive?",
                "icon_color": (255, 150, 50),
                "difficulty": "Hard",
            },
            {
                "id": "memory_flight",
                "name": "Memory Flight",
                "desc": "Remember the color sequence!",
                "details": "Simon Says with wings. Train your memory!",
                "icon_color": (200, 100, 255),
                "difficulty": "Medium",
            },
            {
                "id": "boss_rush",
                "name": "Boss Rush",
                "desc": "Face the Giant Raven!",
                "details": "Epic boss fight with 3 phases. Aim for S rank!",
                "icon_color": (80, 80, 100),
                "difficulty": "Very Hard",
            },
            {
                "id": "treasure_hunt",
                "name": "Treasure Hunt",
                "desc": "Explore the maze for treasure!",
                "details": "Find 5 treasures, avoid traps. 90 seconds!",
                "icon_color": (218, 165, 32),
                "difficulty": "Medium",
            },
        ]
        
        # Initialize hover scales
        for mode in self.modes:
            self.hover_scale[mode["id"]] = 0
        
        self.update_rects()
        self.back_rect = pygame.Rect(20, 15, 80, 38)
        
        # Scrollbar
        self.scrollbar_rect = pygame.Rect(SCREEN_WIDTH - 12, 60, 8, SCREEN_HEIGHT - 80)
        self.scrollbar_handle = None
        self.update_scrollbar()
        
    def update_rects(self):
        start_y = 70
        card_height = 75
        padding = 10
        
        total_height = len(self.modes) * (card_height + padding)
        visible_height = SCREEN_HEIGHT - 80
        self.max_scroll = max(0, total_height - visible_height + 20)
        
        for i, mode in enumerate(self.modes):
            y = start_y + i * (card_height + padding)
            mode["rect"] = pygame.Rect(15, y, SCREEN_WIDTH - 45, card_height)
            
    def update_scrollbar(self):
        if self.max_scroll <= 0:
            self.scrollbar_handle = None
            return
            
        visible_ratio = (SCREEN_HEIGHT - 80) / ((SCREEN_HEIGHT - 80) + self.max_scroll)
        handle_height = max(30, int(self.scrollbar_rect.height * visible_ratio))
        
        scroll_ratio = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
        handle_y = self.scrollbar_rect.y + int((self.scrollbar_rect.height - handle_height) * scroll_ratio)
        
        self.scrollbar_handle = pygame.Rect(self.scrollbar_rect.x, handle_y, 8, handle_height)
        
    def update(self, mouse_pos):
        # Smooth scrolling
        if abs(self.scroll_velocity) > 0.5:
            self.scroll_offset += self.scroll_velocity
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
            self.scroll_velocity *= 0.9
            self.update_scrollbar()
        else:
            self.scroll_velocity = 0
            
        # Update hover states
        self.hovered_mode = None
        for mode in self.modes:
            adjusted_y = mode["rect"].y - self.scroll_offset
            rect = pygame.Rect(mode["rect"].x, adjusted_y, mode["rect"].width, mode["rect"].height)
            
            # Check if visible
            if adjusted_y + rect.height > 55 and adjusted_y < SCREEN_HEIGHT - 20:
                if rect.collidepoint(mouse_pos) and not self.show_confirm:
                    self.hovered_mode = mode["id"]
                    
            # Animate hover scale
            target = 1.0 if mode["id"] == self.hovered_mode else 0.0
            current = self.hover_scale[mode["id"]]
            self.hover_scale[mode["id"]] = current + (target - current) * 0.15
        
    def draw(self, background, ground):
        # Background
        self.screen.fill((25, 28, 35))
        
        # Decorative gradient at top
        for y in range(60):
            alpha = int(255 * (1 - y / 60))
            pygame.draw.line(self.screen, (40, 45, 55), (0, y), (SCREEN_WIDTH, y))
        
        # Header
        pygame.draw.rect(self.screen, (35, 40, 50), (0, 0, SCREEN_WIDTH, 55))
        pygame.draw.line(self.screen, (60, 65, 80), (0, 55), (SCREEN_WIDTH, 55), 2)
        
        title = self.title_font.render("GAME MODES", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 12))
        
        # Back button with hover
        back_color = (80, 85, 100) if self.back_rect.collidepoint(pygame.mouse.get_pos()) else (60, 65, 80)
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=8)
        pygame.draw.rect(self.screen, (100, 105, 120), self.back_rect, 2, border_radius=8)
        back_text = self.small_font.render("← BACK", True, WHITE)
        self.screen.blit(back_text, (self.back_rect.centerx - back_text.get_width() // 2,
                                      self.back_rect.centery - back_text.get_height() // 2))
        
        # Clip area for cards
        clip_rect = pygame.Rect(0, 58, SCREEN_WIDTH - 15, SCREEN_HEIGHT - 60)
        self.screen.set_clip(clip_rect)
        
        # Mode cards
        for mode in self.modes:
            adjusted_y = mode["rect"].y - self.scroll_offset
            
            if adjusted_y + mode["rect"].height < 55 or adjusted_y > SCREEN_HEIGHT:
                continue
                
            self.draw_mode_card(mode, adjusted_y)
            
        self.screen.set_clip(None)
        
        # Scrollbar
        if self.max_scroll > 0:
            self.draw_scrollbar()
            
        # Confirmation dialog
        if self.show_confirm:
            self.draw_confirmation()
            
    def draw_mode_card(self, mode, adjusted_y):
        rect = pygame.Rect(mode["rect"].x, adjusted_y, mode["rect"].width, mode["rect"].height)
        is_hovered = mode["id"] == self.hovered_mode
        scale = self.hover_scale[mode["id"]]
        
        # Card background with hover effect
        if is_hovered:
            # Glow effect
            glow_rect = rect.inflate(4, 4)
            pygame.draw.rect(self.screen, (*mode["icon_color"][:3], 100), glow_rect, border_radius=14)
            
        # Main card
        bg_color = (55, 60, 75) if is_hovered else (45, 50, 62)
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=12)
        
        # Border
        border_color = mode["icon_color"] if is_hovered else (70, 75, 90)
        pygame.draw.rect(self.screen, border_color, rect, 2 + int(scale), border_radius=12)
        
        # Icon circle with pulse effect
        icon_radius = 26 + int(scale * 3)
        icon_center = (rect.x + 40, rect.centery)
        
        # Icon glow
        if is_hovered:
            pygame.draw.circle(self.screen, (*mode["icon_color"][:3], 50), icon_center, icon_radius + 5)
        pygame.draw.circle(self.screen, mode["icon_color"], icon_center, icon_radius)
        self.draw_mode_icon(mode["id"], icon_center, is_hovered)
        
        # Text content
        text_x = rect.x + 80
        
        # Name
        name_color = WHITE if is_hovered else (220, 220, 225)
        name = self.label_font.render(mode["name"], True, name_color)
        self.screen.blit(name, (text_x, rect.y + 10))
        
        # Description
        desc = self.small_font.render(mode["desc"], True, (160, 165, 180))
        self.screen.blit(desc, (text_x, rect.y + 35))
        
        # Difficulty badge
        diff_colors = {
            "Easy": (100, 200, 100),
            "Medium": (255, 200, 100),
            "Hard": (255, 120, 100),
            "Very Hard": (255, 80, 80)
        }
        diff_color = diff_colors.get(mode["difficulty"], (150, 150, 150))
        diff_text = self.desc_font.render(mode["difficulty"], True, diff_color)
        diff_rect = pygame.Rect(rect.right - diff_text.get_width() - 20, rect.y + 12, 
                                diff_text.get_width() + 10, 20)
        pygame.draw.rect(self.screen, (*diff_color, 30), diff_rect, border_radius=4)
        self.screen.blit(diff_text, (diff_rect.x + 5, diff_rect.y + 3))
        
        # Play hint when hovered
        if is_hovered:
            play_text = self.desc_font.render("Click to play →", True, mode["icon_color"])
            self.screen.blit(play_text, (rect.right - play_text.get_width() - 15, rect.bottom - 20))
        
    def draw_mode_icon(self, mode_id, center, is_hovered):
        x, y = center
        color = WHITE
        
        if mode_id == "classic":
            # Bird
            pygame.draw.ellipse(self.screen, (255, 220, 50), (x - 12, y - 7, 24, 14))
            pygame.draw.circle(self.screen, color, (x + 5, y - 2), 4)
            pygame.draw.circle(self.screen, (50, 50, 50), (x + 6, y - 2), 2)
            
        elif mode_id == "time_attack":
            # Clock
            pygame.draw.circle(self.screen, color, (x, y), 12, 2)
            pygame.draw.line(self.screen, color, (x, y), (x, y - 8), 2)
            pygame.draw.line(self.screen, color, (x, y), (x + 6, y), 2)
            
        elif mode_id == "zen":
            # Peaceful waves
            pygame.draw.arc(self.screen, color, (x - 12, y - 8, 24, 16), 0.5, 2.6, 2)
            pygame.draw.circle(self.screen, color, (x, y + 5), 5, 2)
            
        elif mode_id == "bird_battle":
            # Crossed swords
            pygame.draw.line(self.screen, color, (x - 10, y - 10), (x + 10, y + 10), 3)
            pygame.draw.line(self.screen, color, (x + 10, y - 10), (x - 10, y + 10), 3)
            pygame.draw.circle(self.screen, color, (x, y), 5)
            
        elif mode_id == "dodge_master":
            # Shield/dodge
            pygame.draw.polygon(self.screen, color, [
                (x, y - 12), (x + 10, y - 6), (x + 8, y + 10),
                (x, y + 14), (x - 8, y + 10), (x - 10, y - 6)
            ], 2)
            
        elif mode_id == "memory_flight":
            # Brain/memory
            pygame.draw.circle(self.screen, (255, 100, 100), (x - 6, y - 3), 6)
            pygame.draw.circle(self.screen, (100, 150, 255), (x + 6, y - 3), 6)
            pygame.draw.circle(self.screen, (255, 255, 100), (x, y + 6), 6)
            
        elif mode_id == "boss_rush":
            # Boss skull
            pygame.draw.circle(self.screen, color, (x, y - 2), 10, 2)
            pygame.draw.circle(self.screen, (255, 50, 50), (x - 4, y - 4), 3)
            pygame.draw.circle(self.screen, (255, 50, 50), (x + 4, y - 4), 3)
            pygame.draw.line(self.screen, color, (x - 4, y + 6), (x + 4, y + 6), 2)
            
        elif mode_id == "treasure_hunt":
            # Treasure chest
            pygame.draw.rect(self.screen, (139, 90, 43), (x - 10, y - 5, 20, 14))
            pygame.draw.rect(self.screen, color, (x - 10, y - 5, 20, 14), 2)
            pygame.draw.rect(self.screen, (255, 215, 0), (x - 3, y - 1, 6, 6))
            
    def draw_scrollbar(self):
        # Track
        pygame.draw.rect(self.screen, (40, 45, 55), self.scrollbar_rect, border_radius=4)
        
        # Handle
        if self.scrollbar_handle:
            handle_color = (100, 105, 120) if self.is_dragging else (80, 85, 100)
            pygame.draw.rect(self.screen, handle_color, self.scrollbar_handle, border_radius=4)
            
    def draw_confirmation(self):
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 320
        dialog_height = 200
        dialog_rect = pygame.Rect(
            (SCREEN_WIDTH - dialog_width) // 2,
            (SCREEN_HEIGHT - dialog_height) // 2,
            dialog_width, dialog_height
        )
        
        pygame.draw.rect(self.screen, (45, 50, 62), dialog_rect, border_radius=16)
        pygame.draw.rect(self.screen, self.confirm_mode["icon_color"], dialog_rect, 3, border_radius=16)
        
        # Title
        title = self.label_font.render(self.confirm_mode["name"], True, WHITE)
        self.screen.blit(title, (dialog_rect.centerx - title.get_width() // 2, dialog_rect.y + 20))
        
        # Details
        details = self.small_font.render(self.confirm_mode["details"], True, (180, 180, 190))
        self.screen.blit(details, (dialog_rect.centerx - details.get_width() // 2, dialog_rect.y + 55))
        
        # Difficulty
        diff_text = self.small_font.render(f"Difficulty: {self.confirm_mode['difficulty']}", True, (150, 155, 170))
        self.screen.blit(diff_text, (dialog_rect.centerx - diff_text.get_width() // 2, dialog_rect.y + 80))
        
        # Buttons
        btn_y = dialog_rect.y + 120
        
        # Play button
        self.play_btn = pygame.Rect(dialog_rect.x + 30, btn_y, 120, 45)
        pygame.draw.rect(self.screen, self.confirm_mode["icon_color"], self.play_btn, border_radius=10)
        play_text = self.label_font.render("PLAY", True, WHITE)
        self.screen.blit(play_text, (self.play_btn.centerx - play_text.get_width() // 2,
                                      self.play_btn.centery - play_text.get_height() // 2))
        
        # Cancel button
        self.cancel_btn = pygame.Rect(dialog_rect.x + 170, btn_y, 120, 45)
        pygame.draw.rect(self.screen, (80, 85, 100), self.cancel_btn, border_radius=10)
        cancel_text = self.label_font.render("CANCEL", True, WHITE)
        self.screen.blit(cancel_text, (self.cancel_btn.centerx - cancel_text.get_width() // 2,
                                        self.cancel_btn.centery - cancel_text.get_height() // 2))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            # Confirmation dialog
            if self.show_confirm:
                if self.play_btn.collidepoint(pos):
                    self.show_confirm = False
                    return ("select_mode", self.confirm_mode["id"])
                elif self.cancel_btn.collidepoint(pos):
                    self.show_confirm = False
                    self.confirm_mode = None
                return None
            
            # Back button
            if self.back_rect.collidepoint(pos):
                return ("back", None)
            
            # Scrollbar drag
            if self.scrollbar_handle and self.scrollbar_handle.collidepoint(pos):
                self.is_dragging = True
                self.drag_start_y = pos[1]
                return None
            
            # Check cards
            for mode in self.modes:
                adjusted_y = mode["rect"].y - self.scroll_offset
                rect = pygame.Rect(mode["rect"].x, adjusted_y, mode["rect"].width, mode["rect"].height)
                
                if rect.collidepoint(pos) and adjusted_y > 55:
                    # Show confirmation
                    self.show_confirm = True
                    self.confirm_mode = mode
                    return None
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging and self.scrollbar_handle:
                delta = event.pos[1] - self.drag_start_y
                self.drag_start_y = event.pos[1]
                
                scroll_range = self.scrollbar_rect.height - self.scrollbar_handle.height
                if scroll_range > 0:
                    self.scroll_offset += (delta / scroll_range) * self.max_scroll
                    self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
                    self.update_scrollbar()
                    
        elif event.type == pygame.MOUSEWHEEL:
            if not self.show_confirm:
                self.scroll_velocity = -event.y * 25
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.show_confirm:
                    self.show_confirm = False
                    self.confirm_mode = None
                else:
                    return ("back", None)
                    
        return None


class TimeAttackMode:
    """Time Attack mini-game"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.time_limit = 60000
        self.start_time = 0
        self.remaining_time = self.time_limit
        self.is_active = False
        self.score = 0
        self.coins = 0
        self.font = pygame.font.Font(None, 36)
        
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.is_active = True
        self.score = 0
        self.coins = 0
        
    def update(self):
        if self.is_active:
            self.remaining_time = max(0, self.time_limit - (pygame.time.get_ticks() - self.start_time))
            if self.remaining_time <= 0:
                self.is_active = False
                return True
        return False
        
    def add_score(self, p=1):
        self.score += p
        
    def add_coins(self, a=1):
        self.coins += a
        
    def draw_timer(self):
        s = self.remaining_time // 1000
        ms = (self.remaining_time % 1000) // 10
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 80, 100, 40)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), rect, border_radius=10)
        color = ACCENT_COLOR if s <= 10 else WHITE
        text = self.font.render(f"{s:02d}:{ms:02d}", True, color)
        self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))


class ZenMode:
    """Zen Mode"""
    
    def __init__(self, screen, difficulty="easy"):
        self.screen = screen
        self.coins_collected = 0
        self.distance = 0
        self.is_active = False
        self.font = pygame.font.Font(None, 28)
        
    def start(self):
        self.is_active = True
        self.coins_collected = 0
        self.distance = 0
        
    def update(self, dt):
        if self.is_active:
            self.distance += dt * 0.01
            
    def add_coin(self):
        self.coins_collected += 1
        
    def draw_hud(self):
        dist = self.font.render(f"Distance: {int(self.distance)}m", True, WHITE)
        self.screen.blit(dist, (20, 20))
        coins = self.font.render(f"Coins: {self.coins_collected}", True, COIN_COLOR)
        self.screen.blit(coins, (SCREEN_WIDTH - 120, 20))
        zen = self.font.render("ZEN MODE", True, (150, 200, 255))
        self.screen.blit(zen, (SCREEN_WIDTH // 2 - zen.get_width() // 2, 20))


class DailyChallenge:
    """Daily Challenge"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        import datetime
        import random
        today = datetime.date.today()
        random.seed(today.toordinal())
        target = random.randint(10, 25)
        self.active_challenge = {"type": "score", "target": target, "current": 0, "desc": f"Reach score {target}"}
        self.completed = False
        self.reward = 50
        
    def update_progress(self, t, a):
        if self.active_challenge["type"] == t:
            self.active_challenge["current"] += a
            if self.active_challenge["current"] >= self.active_challenge["target"]:
                self.completed = True
                return self.reward
        return 0
        
    def draw_objective(self):
        rect = pygame.Rect(20, SCREEN_HEIGHT - 55, SCREEN_WIDTH - 40, 40)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), rect, border_radius=8)
        progress = min(1.0, self.active_challenge["current"] / self.active_challenge["target"])
        pw = int((rect.width - 10) * progress)
        pygame.draw.rect(self.screen, (80, 80, 80), (rect.x + 5, rect.y + 28, rect.width - 10, 6), border_radius=3)
        pygame.draw.rect(self.screen, PRIMARY_COLOR, (rect.x + 5, rect.y + 28, pw, 6), border_radius=3)
        desc = self.font.render(self.active_challenge["desc"], True, WHITE)
        self.screen.blit(desc, (rect.x + 10, rect.y + 6))
