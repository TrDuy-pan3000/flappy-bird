import pygame
import math
import random
from settings import *

class MainMenu:
    def __init__(self, screen, high_score=0, coins=0):
        self.screen = screen
        self.high_score = high_score
        self.coins = coins
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.coin_font = pygame.font.Font(None, 28)
        self.greeting_font = pygame.font.Font(None, 24)
        
        # Buttons
        center_x = SCREEN_WIDTH // 2
        
        self.play_button = Button(
            center_x - BUTTON_WIDTH // 2,
            290,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "CHƠI" if TET_MODE else "PLAY",
            SECONDARY_COLOR
        )
        
        self.shop_button = Button(
            center_x - BUTTON_WIDTH // 2,
            355,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "CỬA HÀNG" if TET_MODE else "SHOP",
            PRIMARY_COLOR
        )
        
        self.settings_button = Button(
            center_x - BUTTON_WIDTH // 2,
            420,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "CÀI ĐẶT" if TET_MODE else "SETTINGS",
            (100, 100, 120) if not TET_MODE else (139, 0, 0)
        )
        
        # Animation
        self.title_offset = 0
        self.title_direction = 1
        self.bird_angle = 0
        self.greeting_index = 0
        self.greeting_timer = 0
        self.confetti = []
        
        # Initialize Tet effects
        if TET_MODE:
            self.init_confetti()
        
    def init_confetti(self):
        """Initialize Tet confetti"""
        for _ in range(30):
            self.confetti.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-50, SCREEN_HEIGHT),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(1, 3),
                'rotation': random.uniform(0, 360),
                'color': random.choice([TET_RED, TET_GOLD, TET_PINK, TET_YELLOW]),
                'size': random.randint(4, 10)
            })
        
    def update(self, mouse_pos):
        """Update menu state"""
        self.play_button.update(mouse_pos)
        self.shop_button.update(mouse_pos)
        self.settings_button.update(mouse_pos)
        
        # Animate title
        self.title_offset += 0.5 * self.title_direction
        if abs(self.title_offset) > 5:
            self.title_direction *= -1
            
        # Animate bird
        self.bird_angle += 2
        
        # Update greeting rotation (Tet)
        if TET_MODE:
            self.greeting_timer += 1
            if self.greeting_timer > 180:  # Change every 3 seconds
                self.greeting_timer = 0
                self.greeting_index = (self.greeting_index + 1) % len(TET_GREETINGS)
            
            # Update confetti
            for c in self.confetti:
                c['x'] += c['vx']
                c['y'] += c['vy']
                c['rotation'] += 3
                
                if c['y'] > SCREEN_HEIGHT:
                    c['y'] = -20
                    c['x'] = random.randint(0, SCREEN_WIDTH)
        
    def draw(self, background, ground):
        """Draw the main menu"""
        # Draw background
        background.draw(self.screen)
        ground.draw(self.screen)
        
        # Draw semi-transparent overlay for readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80 if TET_MODE else 50))
        self.screen.blit(overlay, (0, 0))
        
        # Draw confetti (Tet)
        if TET_MODE:
            for c in self.confetti:
                self.draw_confetti_piece(c)
        
        # Coins display in top right
        coin_bg = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 35)
        pygame.draw.rect(self.screen, (0, 0, 0), coin_bg, border_radius=8)
        if TET_MODE:
            pygame.draw.rect(self.screen, TET_GOLD, coin_bg, 2, border_radius=8)
        coin_text = f"🪙 {self.coins}"
        coin_surf = self.coin_font.render(coin_text, True, COIN_COLOR)
        self.screen.blit(coin_surf, (SCREEN_WIDTH - 100, 18))
        
        # Draw Tet greeting banner
        if TET_MODE:
            self.draw_tet_banner()
        
        # Draw title
        title_text = "FLAPPY BIRD" if not TET_MODE else "FLAPPY TẾT"
        title_surf = self.title_font.render(title_text, True, WHITE)
        title_shadow = self.title_font.render(title_text, True, TEXT_SHADOW)
        
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100 + self.title_offset))
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 103 + self.title_offset))
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_surf, title_rect)
        
        # Draw subtitle
        if TET_MODE:
            subtitle = f"🧧 Tết 2026 Edition v{VERSION} 🧧"
        else:
            subtitle = "Ultimate Edition v2.0"
        subtitle_surf = self.subtitle_font.render(subtitle, True, PRIMARY_COLOR)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        # Draw animated bird icon
        bird_y = 210 + pygame.math.Vector2(0, 1).rotate(self.bird_angle).y * 8
        self.draw_bird_icon(SCREEN_WIDTH // 2, int(bird_y))
        
        # Draw buttons
        self.play_button.draw(self.screen)
        self.shop_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        
        # Draw high score
        if self.high_score > 0:
            hs_text = f"Kỷ lục: {self.high_score}" if TET_MODE else f"Best: {self.high_score}"
            hs_surf = self.subtitle_font.render(hs_text, True, WHITE)
            hs_rect = hs_surf.get_rect(center=(SCREEN_WIDTH // 2, 500))
            self.screen.blit(hs_surf, hs_rect)
            
        # Draw instructions
        inst_text = "Nhấn SPACE hoặc Click để chơi" if TET_MODE else "Press SPACE or Click to Play"
        inst_surf = pygame.font.Font(None, 22).render(inst_text, True, (180, 180, 180))
        inst_rect = inst_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(inst_surf, inst_rect)
    
    def draw_tet_banner(self):
        """Draw rotating Tet greeting banner"""
        greeting = TET_GREETINGS[self.greeting_index]
        
        # Banner background
        banner_rect = pygame.Rect(20, 50, SCREEN_WIDTH - 40, 35)
        pygame.draw.rect(self.screen, TET_RED, banner_rect, border_radius=8)
        pygame.draw.rect(self.screen, TET_GOLD, banner_rect, 2, border_radius=8)
        
        # Greeting text
        text_surf = self.greeting_font.render(greeting, True, TET_GOLD)
        text_rect = text_surf.get_rect(center=banner_rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def draw_confetti_piece(self, c):
        """Draw a confetti piece"""
        surf = pygame.Surface((c['size'], c['size']), pygame.SRCALPHA)
        pygame.draw.rect(surf, c['color'], (0, 0, c['size'], c['size']))
        rotated = pygame.transform.rotate(surf, c['rotation'])
        self.screen.blit(rotated, (int(c['x']), int(c['y'])))
        
    def draw_bird_icon(self, x, y):
        """Draw a simple bird icon (Tet version with golden color)"""
        if TET_MODE:
            # Golden dragon-like bird for Tet
            body_color = TET_GOLD
            accent_color = TET_RED
        else:
            body_color = (255, 220, 50)
            accent_color = (255, 180, 30)
        
        # Body
        pygame.draw.ellipse(self.screen, body_color, (x - 25, y - 15, 50, 30))
        pygame.draw.ellipse(self.screen, accent_color, (x - 25, y - 15, 50, 30), 2)
        
        # Wing
        pygame.draw.ellipse(self.screen, (255, 200, 40), (x - 20, y - 5, 15, 12))
        
        # Eye
        pygame.draw.circle(self.screen, WHITE, (x + 10, y - 5), 8)
        pygame.draw.circle(self.screen, BLACK, (x + 12, y - 5), 4)
        
        # Beak
        beak_color = TET_RED if TET_MODE else (255, 140, 50)
        pygame.draw.polygon(self.screen, beak_color, [(x + 20, y), (x + 32, y + 3), (x + 20, y + 6)])
        
        # Tet decoration (small crown/hat)
        if TET_MODE:
            pygame.draw.polygon(self.screen, TET_RED, [
                (x - 5, y - 18), (x + 5, y - 25), (x + 15, y - 18)
            ])
            pygame.draw.circle(self.screen, TET_GOLD, (x + 5, y - 20), 4)
        
    def handle_event(self, event):
        """Handle menu events, return action"""
        if self.play_button.is_clicked(event):
            return "play"
        if self.shop_button.is_clicked(event):
            return "shop"
        if self.settings_button.is_clicked(event):
            return "settings"
            
        # Space to play
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return "play"
            
        return None


class SettingsMenu:
    def __init__(self, screen, current_difficulty="medium"):
        self.screen = screen
        self.current_difficulty = current_difficulty
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 32)
        
        center_x = SCREEN_WIDTH // 2
        
        # Difficulty buttons with Tet colors
        easy_color = (100, 200, 100) if not TET_MODE else (100, 180, 100)
        medium_color = PRIMARY_COLOR
        hard_color = ACCENT_COLOR if not TET_MODE else TET_RED
        
        self.easy_button = Button(
            center_x - 180,
            250,
            100,
            45,
            "DỄ" if TET_MODE else "EASY",
            easy_color
        )
        
        self.medium_button = Button(
            center_x - 50,
            250,
            100,
            45,
            "VỪA" if TET_MODE else "MEDIUM",
            medium_color
        )
        
        self.hard_button = Button(
            center_x + 80,
            250,
            100,
            45,
            "KHÓ" if TET_MODE else "HARD",
            hard_color
        )
        
        # Back button
        self.back_button = Button(
            center_x - BUTTON_WIDTH // 2,
            450,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "TRỞ VỀ" if TET_MODE else "BACK",
            (100, 100, 120) if not TET_MODE else PANEL_DARK
        )
        
    def update(self, mouse_pos):
        self.easy_button.update(mouse_pos)
        self.medium_button.update(mouse_pos)
        self.hard_button.update(mouse_pos)
        self.back_button.update(mouse_pos)
        
    def draw(self, background, ground):
        # Draw background
        background.draw(self.screen)
        ground.draw(self.screen)
        
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150 if TET_MODE else 100))
        self.screen.blit(overlay, (0, 0))
        
        # Panel with Tet styling
        panel = Panel(50, 100, SCREEN_WIDTH - 100, 380, tet_style=TET_MODE)
        panel.draw(self.screen)
        
        # Title
        title_text = "CÀI ĐẶT" if TET_MODE else "SETTINGS"
        title_surf = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)
        
        # Difficulty label
        diff_text = "Độ khó:" if TET_MODE else "Difficulty:"
        diff_label = self.label_font.render(diff_text, True, WHITE)
        self.screen.blit(diff_label, (80, 210))
        
        # Draw buttons
        self.easy_button.draw(self.screen)
        self.medium_button.draw(self.screen)
        self.hard_button.draw(self.screen)
        
        # Highlight current selection
        self.draw_selection_indicator()
        
        # Current difficulty description
        if TET_MODE:
            descriptions = {
                "easy": "Chế độ nhẹ nhàng cho người mới",
                "medium": "Cân bằng giữa thử thách và vui",
                "hard": "Thử thách bản thân!"
            }
        else:
            descriptions = {
                "easy": "Slower speed, larger gaps",
                "medium": "Balanced gameplay",
                "hard": "Fast speed, small gaps"
            }
        desc = descriptions.get(self.current_difficulty, "")
        desc_surf = pygame.font.Font(None, 24).render(desc, True, (200, 200, 200))
        desc_rect = desc_surf.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(desc_surf, desc_rect)
        
        # Back button
        self.back_button.draw(self.screen)
        
    def draw_selection_indicator(self):
        """Draw indicator for current difficulty"""
        buttons = {
            "easy": self.easy_button,
            "medium": self.medium_button,
            "hard": self.hard_button
        }
        
        if self.current_difficulty in buttons:
            btn = buttons[self.current_difficulty]
            indicator_rect = btn.rect.inflate(10, 10)
            border_color = TET_GOLD if TET_MODE else WHITE
            pygame.draw.rect(self.screen, border_color, indicator_rect, 3, border_radius=BUTTON_RADIUS + 2)
        
    def handle_event(self, event):
        if self.easy_button.is_clicked(event):
            self.current_difficulty = "easy"
            return ("difficulty", "easy")
        if self.medium_button.is_clicked(event):
            self.current_difficulty = "medium"
            return ("difficulty", "medium")
        if self.hard_button.is_clicked(event):
            self.current_difficulty = "hard"
            return ("difficulty", "hard")
        if self.back_button.is_clicked(event):
            return ("back", None)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return ("back", None)
            
        return None


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.high_score = 0
        self.is_new_high_score = False
        self.medal_type = None
        self.coins_earned = 0
        self.lixi_earned = 0  # Tet special
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 40)
        self.label_font = pygame.font.Font(None, 28)
        
        center_x = SCREEN_WIDTH // 2
        
        # Buttons with Tet styling
        self.retry_button = Button(
            center_x - BUTTON_WIDTH - 10,
            420,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "THỬ LẠI" if TET_MODE else "RETRY",
            SECONDARY_COLOR
        )
        
        self.menu_button = Button(
            center_x + 10,
            420,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "MENU",
            ACCENT_COLOR if not TET_MODE else TET_RED
        )
        
        # Medal display
        self.medal_display = MedalDisplay(center_x - 32, 240)
        
        # Animation
        self.panel_y = -300
        self.target_panel_y = 100
        
        # Tet firework celebration
        self.celebration_particles = []
        
    def set_scores(self, score, high_score, is_new_high, medal_type, coins_earned=0, lixi_earned=0):
        self.score = score
        self.high_score = high_score
        self.is_new_high_score = is_new_high
        self.medal_type = medal_type
        self.coins_earned = coins_earned
        self.lixi_earned = lixi_earned
        self.medal_display.set_medal(medal_type)
        self.panel_y = -300
        
        # Spawn celebration particles for Tet
        if TET_MODE and is_new_high:
            self.spawn_celebration()
    
    def spawn_celebration(self):
        """Spawn celebration particles"""
        for _ in range(50):
            self.celebration_particles.append({
                'x': SCREEN_WIDTH // 2,
                'y': SCREEN_HEIGHT // 2,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-8, -2),
                'life': 1.0,
                'color': random.choice([TET_RED, TET_GOLD, TET_PINK, WHITE]),
                'size': random.randint(4, 10)
            })
        
    def update(self, mouse_pos):
        self.retry_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        
        # Animate panel sliding in
        self.panel_y += (self.target_panel_y - self.panel_y) * 0.15
        
        # Update celebration particles
        for p in self.celebration_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.2
            p['life'] -= 0.015
            if p['life'] <= 0:
                self.celebration_particles.remove(p)
        
    def draw(self):
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180 if TET_MODE else 150))
        self.screen.blit(overlay, (0, 0))
        
        # Draw celebration particles
        for p in self.celebration_particles:
            alpha = int(255 * p['life'])
            pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), int(p['size'] * p['life']))
        
        # Panel
        panel_rect = pygame.Rect(30, int(self.panel_y), SCREEN_WIDTH - 60, 380)
        
        # Shadow
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=15)
        
        # Main panel with Tet styling
        panel_color = PANEL_COLOR if TET_MODE else (222, 184, 135)
        border_color = TET_GOLD if TET_MODE else PANEL_DARK
        pygame.draw.rect(self.screen, panel_color, panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, border_color, panel_rect, 4, border_radius=15)
        
        # Title
        title_text = "KẾT THÚC" if TET_MODE else "GAME OVER"
        title_color = TET_GOLD if TET_MODE else ACCENT_COLOR
        title_surf = self.title_font.render(title_text, True, title_color)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, int(self.panel_y) + 35))
        self.screen.blit(title_surf, title_rect)
        
        # Score section
        score_y = int(self.panel_y) + 75
        
        # Score label and value
        score_label_text = "Điểm" if TET_MODE else "Score"
        score_label = self.label_font.render(score_label_text, True, TEXT_SHADOW if not TET_MODE else (200, 180, 150))
        self.screen.blit(score_label, (60, score_y))
        score_val = self.score_font.render(str(self.score), True, WHITE)
        self.screen.blit(score_val, (60, score_y + 22))
        
        # Best label and value
        best_label_text = "Kỷ lục" if TET_MODE else "Best"
        best_label = self.label_font.render(best_label_text, True, TEXT_SHADOW if not TET_MODE else (200, 180, 150))
        self.screen.blit(best_label, (60, score_y + 60))
        best_val = self.score_font.render(str(self.high_score), True, WHITE)
        self.screen.blit(best_val, (60, score_y + 82))
        
        # Coins/Lixi earned
        earnings_y = score_y + 120
        if self.coins_earned > 0:
            coin_label = self.label_font.render("Xu", True, TEXT_SHADOW if not TET_MODE else (200, 180, 150))
            self.screen.blit(coin_label, (60, earnings_y))
            coin_val = self.score_font.render(f"+{self.coins_earned}", True, COIN_COLOR)
            self.screen.blit(coin_val, (60, earnings_y + 22))
        
        if TET_MODE and self.lixi_earned > 0:
            lixi_label = self.label_font.render("Lì Xì 🧧", True, (200, 180, 150))
            self.screen.blit(lixi_label, (150, earnings_y))
            lixi_val = self.score_font.render(f"+{self.lixi_earned}", True, TET_RED)
            self.screen.blit(lixi_val, (150, earnings_y + 22))
        
        # Medal
        if self.medal_type:
            self.medal_display.y = int(self.panel_y) + 85
            self.medal_display.x = SCREEN_WIDTH - 110
            self.medal_display.draw(self.screen)
            
            # Medal label
            medal_label = self.label_font.render(self.medal_type.upper(), True, PRIMARY_COLOR)
            medal_rect = medal_label.get_rect(center=(SCREEN_WIDTH - 78, int(self.panel_y) + 160))
            self.screen.blit(medal_label, medal_rect)
        
        # New high score indicator
        if self.is_new_high_score:
            if TET_MODE:
                new_text = "🎊 KỶ LỤC MỚI! 🎊"
            else:
                new_text = "🎉 NEW BEST! 🎉"
            new_surf = self.label_font.render(new_text, True, PRIMARY_COLOR)
            new_rect = new_surf.get_rect(center=(SCREEN_WIDTH // 2, int(self.panel_y) + 260))
            self.screen.blit(new_surf, new_rect)
        
        # Buttons
        self.retry_button.rect.y = int(self.panel_y) + 290
        self.menu_button.rect.y = int(self.panel_y) + 290
        
        self.retry_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        
    def handle_event(self, event):
        if self.retry_button.is_clicked(event):
            return "retry"
        if self.menu_button.is_clicked(event):
            return "menu"
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                return "retry"
            if event.key == pygame.K_ESCAPE:
                return "menu"
                
        return None


class PauseScreen:
    """Enhanced pause menu with Tet styling"""
    
    def __init__(self, screen):
        self.screen = screen
        
        center_x = SCREEN_WIDTH // 2
        
        # Fonts
        self.title_font = pygame.font.Font(None, 56)
        self.label_font = pygame.font.Font(None, 24)
        
        # Buttons
        self.resume_button = Button(
            center_x - BUTTON_WIDTH // 2,
            230,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "▶ TIẾP TỤC" if TET_MODE else "▶ RESUME",
            SECONDARY_COLOR
        )
        
        self.restart_button = Button(
            center_x - BUTTON_WIDTH // 2,
            295,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "↻ CHƠI LẠI" if TET_MODE else "↻ RESTART",
            PRIMARY_COLOR
        )
        
        self.menu_button = Button(
            center_x - BUTTON_WIDTH // 2,
            360,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "🏠 MENU",
            ACCENT_COLOR if not TET_MODE else TET_RED
        )
        
        # Animation
        self.pulse = 0
        
    def update(self, mouse_pos):
        self.resume_button.update(mouse_pos)
        self.restart_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        self.pulse = (self.pulse + 0.1) % (3.14159 * 2)
        
    def draw(self):
        # Dark overlay with gradient
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220 if TET_MODE else 200))
        self.screen.blit(overlay, (0, 0))
        
        # Panel background with Tet styling
        panel_rect = pygame.Rect(40, 130, SCREEN_WIDTH - 80, 320)
        panel_color = PANEL_COLOR if TET_MODE else (35, 40, 50)
        border_color = TET_GOLD if TET_MODE else (60, 65, 80)
        pygame.draw.rect(self.screen, panel_color, panel_rect, border_radius=20)
        pygame.draw.rect(self.screen, border_color, panel_rect, 3, border_radius=20)
        
        # Decorative lines
        pulse_alpha = int(100 + 50 * math.sin(self.pulse))
        line_color = TET_GOLD if TET_MODE else (100, 150, 255)
        pygame.draw.line(self.screen, line_color, 
                        (60, 175), (SCREEN_WIDTH - 60, 175), 2)
        
        # Title
        title_text = "TẠM DỪNG" if TET_MODE else "PAUSED"
        title_surf = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 155))
        
        # Title shadow
        shadow_color = PANEL_DARK if TET_MODE else (30, 30, 40)
        shadow = self.title_font.render(title_text, True, shadow_color)
        self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_surf, title_rect)
        
        # Buttons
        self.resume_button.draw(self.screen)
        self.restart_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        
        # Keyboard hints
        if TET_MODE:
            hints = [
                ("SPACE/P", "Tiếp tục"),
                ("R", "Chơi lại"),
                ("ESC", "Menu")
            ]
        else:
            hints = [
                ("SPACE/P", "Resume"),
                ("R", "Restart"),
                ("ESC", "Menu")
            ]
        
        hint_y = 420
        for key, action in hints:
            key_rect = pygame.Rect(60, hint_y, 60, 22)
            key_bg = PANEL_DARK if TET_MODE else (50, 55, 65)
            pygame.draw.rect(self.screen, key_bg, key_rect, border_radius=4)
            pygame.draw.rect(self.screen, (80, 85, 95), key_rect, 1, border_radius=4)
            
            key_text = self.label_font.render(key, True, (180, 180, 190))
            self.screen.blit(key_text, (key_rect.centerx - key_text.get_width() // 2, 
                                        key_rect.centery - key_text.get_height() // 2))
            
            action_text = self.label_font.render(action, True, (140, 140, 150))
            self.screen.blit(action_text, (130, hint_y + 3))
            
            hint_y += 28
        
    def handle_event(self, event):
        if self.resume_button.is_clicked(event):
            return "resume"
        if self.restart_button.is_clicked(event):
            return "restart"
        if self.menu_button.is_clicked(event):
            return "menu"
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_SPACE):
                return "resume"
            if event.key == pygame.K_r:
                return "restart"
            if event.key == pygame.K_ESCAPE:
                return "menu"
                
        return None


# =============================================================================
# UI COMPONENTS
# =============================================================================

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.font = pygame.font.Font(None, 28)
        
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=BUTTON_RADIUS)
        
        # Draw button with hover effect
        color = self.color
        if self.hovered:
            color = tuple(min(255, c + 30) for c in self.color[:3])
        
        pygame.draw.rect(screen, color, self.rect, border_radius=BUTTON_RADIUS)
        
        # Border
        border_color = TET_GOLD if TET_MODE else (255, 255, 255, 100)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=BUTTON_RADIUS)
        
        # Text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class Panel:
    def __init__(self, x, y, width, height, tet_style=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.tet_style = tet_style
        
    def draw(self, screen):
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=15)
        
        # Main panel
        if self.tet_style:
            pygame.draw.rect(screen, PANEL_COLOR, self.rect, border_radius=15)
            pygame.draw.rect(screen, TET_GOLD, self.rect, 3, border_radius=15)
        else:
            pygame.draw.rect(screen, (222, 184, 135), self.rect, border_radius=15)
            pygame.draw.rect(screen, (139, 90, 43), self.rect, 3, border_radius=15)


class MedalDisplay:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.medal_type = None
        self.pulse = 0
        
    def set_medal(self, medal_type):
        self.medal_type = medal_type
        
    def draw(self, screen):
        if not self.medal_type:
            return
            
        self.pulse = (self.pulse + 0.1) % (math.pi * 2)
        scale = 1 + math.sin(self.pulse) * 0.05
        
        colors = {
            "bronze": (205, 127, 50),
            "silver": (192, 192, 192),
            "gold": (255, 215, 0),
            "platinum": (229, 228, 226)
        }
        
        color = colors.get(self.medal_type, (200, 200, 200))
        radius = int(32 * scale)
        
        # Glow effect
        glow_color = (*color, 50)
        pygame.draw.circle(screen, color, (self.x + 32, self.y + 32), radius + 5)
        
        # Medal
        pygame.draw.circle(screen, color, (self.x + 32, self.y + 32), radius)
        
        # Inner details
        inner_color = tuple(max(0, c - 30) for c in color)
        pygame.draw.circle(screen, inner_color, (self.x + 32, self.y + 32), radius - 8, 2)


class ScoreDisplay:
    def __init__(self, x, y, font_size=48):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, font_size)
        self.score = 0
        
    def draw(self, screen):
        text = self.font.render(str(self.score), True, WHITE)
        shadow = self.font.render(str(self.score), True, (50, 50, 50))
        screen.blit(shadow, (self.x + 2, self.y + 2))
        screen.blit(text, (self.x, self.y))
