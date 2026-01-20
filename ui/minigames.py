import pygame
import math
import random
from settings import *

class MiniGameMenu:
    """Enhanced game mode selection menu with Tet theme"""
    
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
                "name": "Chế độ Cổ điển" if TET_MODE else "Classic Mode",
                "desc": "Trải nghiệm Flappy Bird gốc" if TET_MODE else "The original Flappy Bird experience",
                "details": "Bay qua ống không ngừng. Đơn giản và gây nghiện!" if TET_MODE else "Fly through pipes endlessly. Simple and addictive!",
                "icon_color": SECONDARY_COLOR,
                "difficulty": "Dễ" if TET_MODE else "Easy",
                "unlocked": True,
            },
            {
                "id": "time_attack",
                "name": "Tốc độ Thời gian" if TET_MODE else "Time Attack",
                "desc": "Ghi điểm tối đa trong 60 giây!" if TET_MODE else "Score as much as possible in 60 seconds!",
                "details": "Đua với thời gian. Mỗi giây đều quan trọng!" if TET_MODE else "Race against time. Every second counts!",
                "icon_color": PRIMARY_COLOR,
                "difficulty": "Vừa" if TET_MODE else "Medium",
                "unlocked": True,
            },
            {
                "id": "zen",
                "name": "Chế độ Thư giãn" if TET_MODE else "Zen Mode", 
                "desc": "Bay thư thái - không chướng ngại" if TET_MODE else "Relaxing flight - no obstacles",
                "details": "Thu thập xu và tận hưởng chuyến bay." if TET_MODE else "Just collect coins and enjoy the flight.",
                "icon_color": (150, 200, 255),
                "difficulty": "Dễ" if TET_MODE else "Easy",
                "unlocked": True,
            },
        ]
        
        # Add Tet exclusive mode
        if TET_MODE:
            self.modes.insert(0, {
                "id": "lixi_hunt",
                "name": "🧧 Săn Lì Xì",
                "desc": "Thu thập lì xì may mắn!",
                "details": "Chế độ đặc biệt Tết! Thu thập bao lì xì để nhận xu bonus!",
                "icon_color": TET_RED,
                "difficulty": "Vừa",
                "unlocked": True,
                "tet_exclusive": True,
            })
        
        # Add more modes
        self.modes.extend([
            {
                "id": "bird_battle",
                "name": "Đại Chiến Chim" if TET_MODE else "Bird Battle",
                "desc": "Chiến đấu PvP với AI!" if TET_MODE else "Epic PvP combat against AI!",
                "details": "Bắn, né, dùng kỹ năng. Chim cuối cùng thắng!" if TET_MODE else "Shoot, dodge, use power-ups. Last bird standing wins!",
                "icon_color": ACCENT_COLOR,
                "difficulty": "Khó" if TET_MODE else "Hard",
                "unlocked": True,
            },
            {
                "id": "dodge_master",
                "name": "Né Siêu Hạng" if TET_MODE else "Dodge Master",
                "desc": "Sống sót qua làn sóng chướng ngại!" if TET_MODE else "Survive waves of falling obstacles!",
                "details": "Thử thách phản xạ. Bạn sống được bao lâu?" if TET_MODE else "Test your reflexes. How long can you survive?",
                "icon_color": (255, 150, 50),
                "difficulty": "Khó" if TET_MODE else "Hard",
                "unlocked": True,
            },
            {
                "id": "memory_flight",
                "name": "Bay Nhớ Màu" if TET_MODE else "Memory Flight",
                "desc": "Ghi nhớ chuỗi màu sắc!" if TET_MODE else "Remember the color sequence!",
                "details": "Simon Says với cánh. Luyện trí nhớ!" if TET_MODE else "Simon Says with wings. Train your memory!",
                "icon_color": (200, 100, 255),
                "difficulty": "Vừa" if TET_MODE else "Medium",
                "unlocked": True,
            },
            {
                "id": "boss_rush",
                "name": "Đánh Boss Khổng Lồ" if TET_MODE else "Boss Rush",
                "desc": "Đối đầu Quạ Khổng Lồ!" if TET_MODE else "Face the Giant Raven!",
                "details": "Boss fight 3 giai đoạn. Nhắm hạng S!" if TET_MODE else "Epic boss fight with 3 phases. Aim for S rank!",
                "icon_color": (80, 80, 100),
                "difficulty": "Rất Khó" if TET_MODE else "Very Hard",
                "unlocked": True,
            },
            {
                "id": "treasure_hunt",
                "name": "Săn Kho Báu" if TET_MODE else "Treasure Hunt",
                "desc": "Khám phá mê cung tìm báu vật!" if TET_MODE else "Explore the maze for treasure!",
                "details": "Tìm 5 kho báu, tránh bẫy. 90 giây!" if TET_MODE else "Find 5 treasures, avoid traps. 90 seconds!",
                "icon_color": (218, 165, 32),
                "difficulty": "Vừa" if TET_MODE else "Medium",
                "unlocked": True,
            },
        ])
        
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
        # Background with Tet theme
        if TET_MODE:
            self.screen.fill((30, 15, 25))
            # Decorative gradient
            for y in range(60):
                alpha = int(255 * (1 - y / 60))
                pygame.draw.line(self.screen, (50, 25, 40), (0, y), (SCREEN_WIDTH, y))
        else:
            self.screen.fill((25, 28, 35))
            for y in range(60):
                alpha = int(255 * (1 - y / 60))
                pygame.draw.line(self.screen, (40, 45, 55), (0, y), (SCREEN_WIDTH, y))
        
        # Header with Tet styling
        header_color = PANEL_COLOR if TET_MODE else (35, 40, 50)
        pygame.draw.rect(self.screen, header_color, (0, 0, SCREEN_WIDTH, 55))
        
        line_color = TET_GOLD if TET_MODE else (60, 65, 80)
        pygame.draw.line(self.screen, line_color, (0, 55), (SCREEN_WIDTH, 55), 2)
        
        title = "CHẾ ĐỘ CHƠI" if TET_MODE else "GAME MODES"
        title_surf = self.title_font.render(title, True, WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 12))
        
        # Back button with hover
        back_hover = self.back_rect.collidepoint(pygame.mouse.get_pos())
        back_color = TET_RED if TET_MODE and back_hover else (PANEL_DARK if TET_MODE else (60, 65, 80))
        if back_hover and not TET_MODE:
            back_color = (80, 85, 100)
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=8)
        
        border_color = TET_GOLD if TET_MODE else (100, 105, 120)
        pygame.draw.rect(self.screen, border_color, self.back_rect, 2, border_radius=8)
        
        back_text_str = "← VỀ" if TET_MODE else "← BACK"
        back_text = self.small_font.render(back_text_str, True, WHITE)
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
        is_tet_exclusive = mode.get("tet_exclusive", False)
        
        # Card background with hover effect
        if is_hovered:
            # Glow effect
            glow_rect = rect.inflate(4, 4)
            pygame.draw.rect(self.screen, (*mode["icon_color"][:3], 100), glow_rect, border_radius=14)
        
        # Main card with Tet styling
        if TET_MODE:
            bg_color = (60, 30, 40) if is_hovered else (45, 25, 35)
        else:
            bg_color = (55, 60, 75) if is_hovered else (45, 50, 62)
        
        # Special glow for Tet exclusive mode
        if is_tet_exclusive:
            bg_color = (80, 30, 30) if is_hovered else (60, 25, 25)
            
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=12)
        
        # Border
        border_color = mode["icon_color"] if is_hovered else (70, 75, 90)
        if is_tet_exclusive:
            border_color = TET_GOLD
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
        
        # Name with Tet exclusive badge
        name_color = WHITE if is_hovered else (220, 220, 225)
        if is_tet_exclusive:
            name_color = TET_GOLD
        name = self.label_font.render(mode["name"], True, name_color)
        self.screen.blit(name, (text_x, rect.y + 10))
        
        # Description
        desc = self.small_font.render(mode["desc"], True, (160, 165, 180))
        self.screen.blit(desc, (text_x, rect.y + 35))
        
        # Difficulty badge
        if TET_MODE:
            diff_colors = {
                "Dễ": (100, 200, 100),
                "Vừa": (255, 200, 100),
                "Khó": (255, 120, 100),
                "Rất Khó": (255, 80, 80)
            }
        else:
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
        
        # Tet exclusive badge
        if is_tet_exclusive:
            tet_badge = self.desc_font.render("TẾT 2026", True, TET_GOLD)
            self.screen.blit(tet_badge, (rect.right - tet_badge.get_width() - 15, rect.bottom - 18))
        
        # Play hint when hovered
        if is_hovered:
            play_text_str = "Nhấn để chơi →" if TET_MODE else "Click to play →"
            play_text = self.desc_font.render(play_text_str, True, mode["icon_color"])
            self.screen.blit(play_text, (rect.right - play_text.get_width() - 15, rect.bottom - 20))
        
    def draw_mode_icon(self, mode_id, center, is_hovered):
        x, y = center
        color = WHITE
        
        if mode_id == "lixi_hunt":
            # Red envelope icon
            pygame.draw.rect(self.screen, TET_RED, (x - 10, y - 12, 20, 24), border_radius=3)
            pygame.draw.rect(self.screen, TET_GOLD, (x - 10, y - 12, 20, 24), 2, border_radius=3)
            pygame.draw.circle(self.screen, TET_GOLD, (x, y), 6)
            
        elif mode_id == "classic":
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
            # Brain/memory colors
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
        track_color = PANEL_DARK if TET_MODE else (40, 45, 55)
        pygame.draw.rect(self.screen, track_color, self.scrollbar_rect, border_radius=4)
        
        # Handle
        if self.scrollbar_handle:
            if TET_MODE:
                handle_color = TET_GOLD if self.is_dragging else TET_RED
            else:
                handle_color = (100, 105, 120) if self.is_dragging else (80, 85, 100)
            pygame.draw.rect(self.screen, handle_color, self.scrollbar_handle, border_radius=4)
            
    def draw_confirmation(self):
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200 if TET_MODE else 180))
        self.screen.blit(overlay, (0, 0))
        
        # Dialog box with Tet styling
        dialog_width = 320
        dialog_height = 220
        dialog_rect = pygame.Rect(
            (SCREEN_WIDTH - dialog_width) // 2,
            (SCREEN_HEIGHT - dialog_height) // 2,
            dialog_width, dialog_height
        )
        
        dialog_bg = PANEL_COLOR if TET_MODE else (45, 50, 62)
        pygame.draw.rect(self.screen, dialog_bg, dialog_rect, border_radius=16)
        
        border_color = TET_GOLD if TET_MODE else self.confirm_mode["icon_color"]
        pygame.draw.rect(self.screen, border_color, dialog_rect, 3, border_radius=16)
        
        # Title
        title = self.label_font.render(self.confirm_mode["name"], True, WHITE)
        self.screen.blit(title, (dialog_rect.centerx - title.get_width() // 2, dialog_rect.y + 20))
        
        # Details
        details = self.small_font.render(self.confirm_mode["details"], True, (180, 180, 190))
        self.screen.blit(details, (dialog_rect.centerx - details.get_width() // 2, dialog_rect.y + 55))
        
        # Difficulty
        diff_label = "Độ khó:" if TET_MODE else "Difficulty:"
        diff_text = self.small_font.render(f"{diff_label} {self.confirm_mode['difficulty']}", True, (150, 155, 170))
        self.screen.blit(diff_text, (dialog_rect.centerx - diff_text.get_width() // 2, dialog_rect.y + 85))
        
        # Tet exclusive note
        if self.confirm_mode.get("tet_exclusive"):
            tet_note = self.small_font.render("🧧 Chế độ đặc biệt Tết 2026! 🧧", True, TET_GOLD)
            self.screen.blit(tet_note, (dialog_rect.centerx - tet_note.get_width() // 2, dialog_rect.y + 110))
        
        # Buttons
        btn_y = dialog_rect.y + 140
        
        # Play button
        self.play_btn = pygame.Rect(dialog_rect.x + 30, btn_y, 120, 45)
        play_color = SECONDARY_COLOR if not TET_MODE else TET_RED
        pygame.draw.rect(self.screen, play_color, self.play_btn, border_radius=10)
        if TET_MODE:
            pygame.draw.rect(self.screen, TET_GOLD, self.play_btn, 2, border_radius=10)
        
        play_text_str = "CHƠI" if TET_MODE else "PLAY"
        play_text = self.label_font.render(play_text_str, True, WHITE)
        self.screen.blit(play_text, (self.play_btn.centerx - play_text.get_width() // 2,
                                      self.play_btn.centery - play_text.get_height() // 2))
        
        # Cancel button
        self.cancel_btn = pygame.Rect(dialog_rect.x + 170, btn_y, 120, 45)
        cancel_color = PANEL_DARK if TET_MODE else (80, 85, 100)
        pygame.draw.rect(self.screen, cancel_color, self.cancel_btn, border_radius=10)
        
        cancel_text_str = "HỦY" if TET_MODE else "CANCEL"
        cancel_text = self.label_font.render(cancel_text_str, True, WHITE)
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


class LiXiHuntMode:
    """Tet Special Mode - Collect Lucky Red Envelopes!"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty
        self.is_active = False
        self.is_over = False
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.lixi_collected = 0
        self.total_value = 0
        self.time_limit = 60000  # 60 seconds
        self.start_time = 0
        self.remaining_time = self.time_limit
        
        # Li Xi envelopes
        self.lixis = []
        self.last_spawn = 0
        self.spawn_interval = 800  # Spawn every 0.8s
        
        # Effects
        self.particles = []
        self.messages = []  # Floating messages like "+88 🧧"
        
    def start(self):
        self.is_active = True
        self.is_over = False
        self.lixi_collected = 0
        self.total_value = 0
        self.start_time = pygame.time.get_ticks()
        self.lixis.clear()
        self.particles.clear()
        self.messages.clear()
        
    def spawn_lixi(self):
        """Spawn a new li xi envelope"""
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = -40
        value = random.choice(LIXI_VALUES)
        
        # Rare golden li xi
        is_golden = random.random() < 0.1
        if is_golden:
            value *= 2
        
        self.lixis.append({
            'x': x,
            'y': y,
            'value': value,
            'vy': random.uniform(2, 4),
            'swing': random.uniform(0, math.pi * 2),
            'golden': is_golden,
            'collected': False
        })
        
    def update(self, dt, bird_rect):
        if not self.is_active or self.is_over:
            return
            
        now = pygame.time.get_ticks()
        
        # Update timer
        self.remaining_time = max(0, self.time_limit - (now - self.start_time))
        if self.remaining_time <= 0:
            self.is_over = True
            return
        
        # Spawn li xi
        if now - self.last_spawn > self.spawn_interval:
            self.spawn_lixi()
            self.last_spawn = now
        
        # Update li xi positions
        for lixi in self.lixis[:]:
            lixi['y'] += lixi['vy']
            lixi['swing'] += 0.1
            lixi['x'] += math.sin(lixi['swing']) * 1.5
            
            # Check collection
            lixi_rect = pygame.Rect(lixi['x'] - 20, lixi['y'] - 25, 40, 50)
            if lixi_rect.colliderect(bird_rect) and not lixi['collected']:
                lixi['collected'] = True
                self.lixi_collected += 1
                self.total_value += lixi['value']
                
                # Spawn celebration particles
                self.spawn_collect_effect(lixi['x'], lixi['y'], lixi['value'], lixi['golden'])
                
            # Remove if off screen
            if lixi['y'] > SCREEN_HEIGHT or lixi['collected']:
                self.lixis.remove(lixi)
        
        # Update particles
        self.particles = [p for p in self.particles if self.update_particle(p)]
        
        # Update floating messages
        self.messages = [m for m in self.messages if self.update_message(m)]
    
    def update_particle(self, p):
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += 0.1
        p['life'] -= 0.03
        return p['life'] > 0
    
    def update_message(self, m):
        m['y'] -= 1.5
        m['life'] -= 0.02
        return m['life'] > 0
        
    def spawn_collect_effect(self, x, y, value, golden):
        """Spawn collection celebration"""
        # Particles
        color = TET_GOLD if golden else TET_RED
        for _ in range(15):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-4, 4),
                'vy': random.uniform(-6, -2),
                'life': 1.0,
                'color': color,
                'size': random.randint(4, 8)
            })
        
        # Floating message
        self.messages.append({
            'x': x,
            'y': y,
            'text': f"+{value} 🧧",
            'life': 1.0,
            'color': TET_GOLD if golden else WHITE
        })
        
    def draw_lixi(self, lixi):
        """Draw a li xi envelope"""
        x, y = int(lixi['x']), int(lixi['y'])
        
        # Envelope body
        color = TET_GOLD if lixi['golden'] else TET_RED
        pygame.draw.rect(self.screen, color, (x - 18, y - 25, 36, 50), border_radius=5)
        
        # Gold border and decoration
        pygame.draw.rect(self.screen, TET_GOLD, (x - 18, y - 25, 36, 50), 2, border_radius=5)
        
        # Circle decoration
        pygame.draw.circle(self.screen, TET_GOLD, (x, y), 10)
        if lixi['golden']:
            pygame.draw.circle(self.screen, WHITE, (x, y), 6)
        
        # Value text
        value_text = self.small_font.render(str(lixi['value']), True, WHITE)
        self.screen.blit(value_text, (x - value_text.get_width() // 2, y + 12))
        
    def draw(self):
        """Draw li xi HUD and effects"""
        # Draw all li xi envelopes
        for lixi in self.lixis:
            self.draw_lixi(lixi)
        
        # Draw particles
        for p in self.particles:
            alpha = int(255 * p['life'])
            size = int(p['size'] * p['life'])
            if size > 0:
                pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), size)
        
        # Draw floating messages
        for m in self.messages:
            alpha = int(255 * m['life'])
            text = self.font.render(m['text'], True, m['color'])
            self.screen.blit(text, (int(m['x']) - text.get_width() // 2, int(m['y'])))
        
        # Draw HUD
        self.draw_hud()
        
    def draw_hud(self):
        """Draw game HUD"""
        # Timer background
        timer_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, 10, 120, 40)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), timer_rect, border_radius=10)
        pygame.draw.rect(self.screen, TET_GOLD, timer_rect, 2, border_radius=10)
        
        # Timer
        seconds = self.remaining_time // 1000
        ms = (self.remaining_time % 1000) // 10
        timer_color = ACCENT_COLOR if seconds <= 10 else TET_GOLD
        timer_text = self.font.render(f"{seconds:02d}:{ms:02d}", True, timer_color)
        self.screen.blit(timer_text, (timer_rect.centerx - timer_text.get_width() // 2,
                                       timer_rect.centery - timer_text.get_height() // 2))
        
        # Li Xi collected
        lixi_rect = pygame.Rect(10, 10, 120, 35)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), lixi_rect, border_radius=8)
        pygame.draw.rect(self.screen, TET_RED, lixi_rect, 2, border_radius=8)
        
        lixi_text = self.small_font.render(f"🧧 x{self.lixi_collected}", True, WHITE)
        self.screen.blit(lixi_text, (20, 18))
        
        # Total value
        value_rect = pygame.Rect(SCREEN_WIDTH - 130, 10, 120, 35)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), value_rect, border_radius=8)
        pygame.draw.rect(self.screen, TET_GOLD, value_rect, 2, border_radius=8)
        
        value_text = self.small_font.render(f"💰 {self.total_value}", True, TET_GOLD)
        self.screen.blit(value_text, (SCREEN_WIDTH - 120, 18))
        
        # Mode label
        mode_text = self.small_font.render("🧧 SĂN LÌ XÌ", True, TET_RED)
        self.screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 55))
        
    def get_results(self):
        """Return game results"""
        return {
            'lixi_collected': self.lixi_collected,
            'total_value': self.total_value,
            'bonus_coins': self.total_value // 2  # Convert to bonus coins
        }


class TimeAttackMode:
    """Time Attack mini-game with Tet styling"""
    
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
        
        if TET_MODE:
            pygame.draw.rect(self.screen, TET_GOLD, rect, 2, border_radius=10)
        
        color = ACCENT_COLOR if s <= 10 else (TET_GOLD if TET_MODE else WHITE)
        text = self.font.render(f"{s:02d}:{ms:02d}", True, color)
        self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))


class ZenMode:
    """Zen Mode with Tet styling"""
    
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
        dist_text = f"Khoảng cách: {int(self.distance)}m" if TET_MODE else f"Distance: {int(self.distance)}m"
        dist = self.font.render(dist_text, True, WHITE)
        self.screen.blit(dist, (20, 20))
        
        coins = self.font.render(f"Xu: {self.coins_collected}" if TET_MODE else f"Coins: {self.coins_collected}", True, COIN_COLOR)
        self.screen.blit(coins, (SCREEN_WIDTH - 120, 20))
        
        zen_text = "CHẾ ĐỘ THIỀN" if TET_MODE else "ZEN MODE"
        zen = self.font.render(zen_text, True, (150, 200, 255))
        self.screen.blit(zen, (SCREEN_WIDTH // 2 - zen.get_width() // 2, 20))


class DailyChallenge:
    """Daily Challenge with Tet styling"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        import datetime
        today = datetime.date.today()
        random.seed(today.toordinal())
        target = random.randint(10, 25)
        
        if TET_MODE:
            self.active_challenge = {"type": "score", "target": target, "current": 0, 
                                    "desc": f"Đạt điểm {target}"}
        else:
            self.active_challenge = {"type": "score", "target": target, "current": 0, 
                                    "desc": f"Reach score {target}"}
        self.completed = False
        self.reward = 88 if TET_MODE else 50  # Lucky number for Tet
        
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
        
        if TET_MODE:
            pygame.draw.rect(self.screen, TET_GOLD, rect, 2, border_radius=8)
        
        progress = min(1.0, self.active_challenge["current"] / self.active_challenge["target"])
        pw = int((rect.width - 10) * progress)
        pygame.draw.rect(self.screen, (80, 80, 80), (rect.x + 5, rect.y + 28, rect.width - 10, 6), border_radius=3)
        
        bar_color = TET_RED if TET_MODE else PRIMARY_COLOR
        pygame.draw.rect(self.screen, bar_color, (rect.x + 5, rect.y + 28, pw, 6), border_radius=3)
        
        desc = self.font.render(self.active_challenge["desc"], True, WHITE)
        self.screen.blit(desc, (rect.x + 10, rect.y + 6))
