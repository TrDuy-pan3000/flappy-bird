import pygame
from settings import *
from ui.components import Button, Panel, MedalDisplay, ScoreDisplay

class MainMenu:
    def __init__(self, screen, high_score=0, coins=0):
        self.screen = screen
        self.high_score = high_score
        self.coins = coins
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.coin_font = pygame.font.Font(None, 28)
        
        # Buttons
        center_x = SCREEN_WIDTH // 2
        
        self.play_button = Button(
            center_x - BUTTON_WIDTH // 2,
            290,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "PLAY",
            SECONDARY_COLOR
        )
        
        self.shop_button = Button(
            center_x - BUTTON_WIDTH // 2,
            355,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "SHOP",
            PRIMARY_COLOR
        )
        
        self.settings_button = Button(
            center_x - BUTTON_WIDTH // 2,
            420,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "SETTINGS",
            (100, 100, 120)
        )
        
        # Animation
        self.title_offset = 0
        self.title_direction = 1
        self.bird_angle = 0
        
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
        
    def draw(self, background, ground):
        """Draw the main menu"""
        # Draw background
        background.draw(self.screen)
        ground.draw(self.screen)
        
        # Draw semi-transparent overlay for readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))
        self.screen.blit(overlay, (0, 0))
        
        # Coins display in top right
        coin_bg = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 35)
        pygame.draw.rect(self.screen, (0, 0, 0, 100), coin_bg, border_radius=8)
        coin_text = f"🪙 {self.coins}"
        coin_surf = self.coin_font.render(coin_text, True, COIN_COLOR)
        self.screen.blit(coin_surf, (SCREEN_WIDTH - 100, 18))
        
        # Draw title
        title_text = "FLAPPY BIRD"
        title_surf = self.title_font.render(title_text, True, WHITE)
        title_shadow = self.title_font.render(title_text, True, TEXT_SHADOW)
        
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100 + self.title_offset))
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 103 + self.title_offset))
        
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_surf, title_rect)
        
        # Draw subtitle
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
            hs_text = f"Best: {self.high_score}"
            hs_surf = self.subtitle_font.render(hs_text, True, WHITE)
            hs_rect = hs_surf.get_rect(center=(SCREEN_WIDTH // 2, 500))
            self.screen.blit(hs_surf, hs_rect)
            
        # Draw instructions
        inst_text = "Press SPACE or Click to Play"
        inst_surf = pygame.font.Font(None, 22).render(inst_text, True, (180, 180, 180))
        inst_rect = inst_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(inst_surf, inst_rect)
        
    def draw_bird_icon(self, x, y):
        """Draw a simple bird icon"""
        # Body
        pygame.draw.ellipse(self.screen, (255, 220, 50), (x - 25, y - 15, 50, 30))
        pygame.draw.ellipse(self.screen, (255, 180, 30), (x - 25, y - 15, 50, 30), 2)
        
        # Wing
        pygame.draw.ellipse(self.screen, (255, 200, 40), (x - 20, y - 5, 15, 12))
        
        # Eye
        pygame.draw.circle(self.screen, WHITE, (x + 10, y - 5), 8)
        pygame.draw.circle(self.screen, BLACK, (x + 12, y - 5), 4)
        
        # Beak
        pygame.draw.polygon(self.screen, (255, 140, 50), [(x + 20, y), (x + 32, y + 3), (x + 20, y + 6)])
        
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
        
        # Difficulty buttons
        self.easy_button = Button(
            center_x - 180,
            250,
            100,
            45,
            "EASY",
            (100, 200, 100)
        )
        
        self.medium_button = Button(
            center_x - 50,
            250,
            100,
            45,
            "MEDIUM",
            PRIMARY_COLOR
        )
        
        self.hard_button = Button(
            center_x + 80,
            250,
            100,
            45,
            "HARD",
            ACCENT_COLOR
        )
        
        # Back button
        self.back_button = Button(
            center_x - BUTTON_WIDTH // 2,
            450,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "BACK",
            (100, 100, 120)
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
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        # Panel
        panel = Panel(50, 100, SCREEN_WIDTH - 100, 380)
        panel.draw(self.screen)
        
        # Title
        title_surf = self.title_font.render("SETTINGS", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)
        
        # Difficulty label
        diff_label = self.label_font.render("Difficulty:", True, WHITE)
        self.screen.blit(diff_label, (80, 210))
        
        # Draw buttons
        self.easy_button.draw(self.screen)
        self.medium_button.draw(self.screen)
        self.hard_button.draw(self.screen)
        
        # Highlight current selection
        self.draw_selection_indicator()
        
        # Current difficulty description
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
            pygame.draw.rect(self.screen, WHITE, indicator_rect, 3, border_radius=BUTTON_RADIUS + 2)
        
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
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 40)
        self.label_font = pygame.font.Font(None, 28)
        
        center_x = SCREEN_WIDTH // 2
        
        # Buttons
        self.retry_button = Button(
            center_x - BUTTON_WIDTH - 10,
            420,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "RETRY",
            SECONDARY_COLOR
        )
        
        self.menu_button = Button(
            center_x + 10,
            420,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "MENU",
            ACCENT_COLOR
        )
        
        # Medal display
        self.medal_display = MedalDisplay(center_x - 32, 240)
        
        # Animation
        self.panel_y = -300
        self.target_panel_y = 100
        
    def set_scores(self, score, high_score, is_new_high, medal_type, coins_earned=0):
        self.score = score
        self.high_score = high_score
        self.is_new_high_score = is_new_high
        self.medal_type = medal_type
        self.coins_earned = coins_earned
        self.medal_display.set_medal(medal_type)
        self.panel_y = -300  # Reset animation
        
    def update(self, mouse_pos):
        self.retry_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        
        # Animate panel sliding in
        self.panel_y += (self.target_panel_y - self.panel_y) * 0.15
        
    def draw(self):
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Panel
        panel_rect = pygame.Rect(30, int(self.panel_y), SCREEN_WIDTH - 60, 380)
        
        # Shadow
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=15)
        
        # Main panel
        pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, PANEL_DARK, panel_rect, 4, border_radius=15)
        
        # Title
        title_text = "GAME OVER"
        title_surf = self.title_font.render(title_text, True, ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, int(self.panel_y) + 35))
        self.screen.blit(title_surf, title_rect)
        
        # Score section
        score_y = int(self.panel_y) + 75
        
        # Score label and value
        score_label = self.label_font.render("Score", True, TEXT_SHADOW)
        self.screen.blit(score_label, (60, score_y))
        score_val = self.score_font.render(str(self.score), True, WHITE)
        self.screen.blit(score_val, (60, score_y + 22))
        
        # Best label and value
        best_label = self.label_font.render("Best", True, TEXT_SHADOW)
        self.screen.blit(best_label, (60, score_y + 60))
        best_val = self.score_font.render(str(self.high_score), True, WHITE)
        self.screen.blit(best_val, (60, score_y + 82))
        
        # Coins earned
        if self.coins_earned > 0:
            coin_label = self.label_font.render("Coins", True, TEXT_SHADOW)
            self.screen.blit(coin_label, (60, score_y + 120))
            coin_val = self.score_font.render(f"+{self.coins_earned}", True, COIN_COLOR)
            self.screen.blit(coin_val, (60, score_y + 142))
        
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
            new_text = "🎉 NEW BEST! 🎉"
            new_surf = self.label_font.render(new_text, True, PRIMARY_COLOR)
            new_rect = new_surf.get_rect(center=(SCREEN_WIDTH // 2, int(self.panel_y) + 240))
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
    """Enhanced pause menu with more options"""
    
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
            "▶ RESUME",
            SECONDARY_COLOR
        )
        
        self.restart_button = Button(
            center_x - BUTTON_WIDTH // 2,
            295,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "↻ RESTART",
            PRIMARY_COLOR
        )
        
        self.menu_button = Button(
            center_x - BUTTON_WIDTH // 2,
            360,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "🏠 MENU",
            ACCENT_COLOR
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
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Panel background
        panel_rect = pygame.Rect(40, 130, SCREEN_WIDTH - 80, 320)
        pygame.draw.rect(self.screen, (35, 40, 50), panel_rect, border_radius=20)
        pygame.draw.rect(self.screen, (60, 65, 80), panel_rect, 3, border_radius=20)
        
        # Decorative lines
        import math
        pulse_alpha = int(100 + 50 * math.sin(self.pulse))
        pygame.draw.line(self.screen, (100, 150, 255, pulse_alpha), 
                        (60, 175), (SCREEN_WIDTH - 60, 175), 2)
        
        # Title
        title_surf = self.title_font.render("PAUSED", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 155))
        
        # Title shadow
        shadow = self.title_font.render("PAUSED", True, (30, 30, 40))
        self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_surf, title_rect)
        
        # Buttons
        self.resume_button.draw(self.screen)
        self.restart_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        
        # Keyboard hints
        hints = [
            ("SPACE/P", "Resume"),
            ("R", "Restart"),
            ("ESC", "Menu")
        ]
        
        hint_y = 420
        for key, action in hints:
            key_rect = pygame.Rect(60, hint_y, 60, 22)
            pygame.draw.rect(self.screen, (50, 55, 65), key_rect, border_radius=4)
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
