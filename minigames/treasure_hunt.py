import pygame
import random
from settings import *

class TreasureHunt:
    """Treasure Hunt maze adventure mini-game"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty
        
        # Game state
        self.is_active = False
        self.is_over = False
        self.victory = False
        
        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 56)
        
        # Map settings
        self.tile_size = 40
        self.map_width = SCREEN_WIDTH // self.tile_size
        self.map_height = (SCREEN_HEIGHT - 60) // self.tile_size
        
        # Player
        self.player_x = 1
        self.player_y = 1
        self.player_hp = 3
        
        # Collectibles
        self.treasures_collected = 0
        self.treasures_total = 5
        self.has_key = False
        
        # Timer
        self.time_limit = 90000  # 90 seconds
        self.start_time = 0
        
        # Map data
        self.map_data = []
        self.enemies = []
        
    def start(self, skin_id="default"):
        """Start new game"""
        self.is_active = True
        self.is_over = False
        self.victory = False
        
        self.player_x = 1
        self.player_y = 1
        self.player_hp = 3
        self.treasures_collected = 0
        self.has_key = False
        
        self.start_time = pygame.time.get_ticks()
        
        self.generate_map()
        
    def generate_map(self):
        """Generate maze map"""
        # Initialize with walls
        self.map_data = [['#' for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        # Carve out rooms and corridors
        # Main room (start)
        for y in range(1, 4):
            for x in range(1, 4):
                self.map_data[y][x] = '.'
                
        # Corridors
        for x in range(4, self.map_width - 1):
            self.map_data[2][x] = '.'
            
        for y in range(2, self.map_height - 2):
            self.map_data[y][self.map_width // 2] = '.'
            
        # Room 2 (top right - key)
        for y in range(1, 4):
            for x in range(self.map_width - 4, self.map_width - 1):
                self.map_data[y][x] = '.'
        self.map_data[2][self.map_width - 3] = 'K'  # Key
        
        # Room 3 (bottom)
        for y in range(self.map_height - 4, self.map_height - 1):
            for x in range(1, self.map_width - 1):
                self.map_data[y][x] = '.'
                
        # Add treasures
        treasure_spots = [
            (2, self.map_height - 3),
            (self.map_width - 3, self.map_height - 2),
            (self.map_width // 2, 2),
            (1, self.map_height - 2),
            (self.map_width - 2, 1)
        ]
        for i, (tx, ty) in enumerate(treasure_spots[:self.treasures_total]):
            if self.map_data[ty][tx] == '.':
                self.map_data[ty][tx] = 'T'
                
        # Add traps
        trap_spots = [(4, 2), (6, 2), (self.map_width // 2, 4), (self.map_width // 2, 6)]
        for tx, ty in trap_spots:
            if ty < len(self.map_data) and tx < len(self.map_data[0]):
                if self.map_data[ty][tx] == '.':
                    self.map_data[ty][tx] = '^'
                
        # Add locked door and exit
        self.map_data[self.map_height - 2][self.map_width // 2] = 'D'  # Door
        self.map_data[self.map_height - 1][self.map_width // 2] = 'E'  # Exit (behind door)
        
        # Add enemies
        self.enemies = [
            {"x": 5, "y": 2, "dir": 1, "range": 3},
            {"x": self.map_width // 2, "y": self.map_height - 3, "dir": 1, "range": 4}
        ]
        
    def update(self, dt):
        if not self.is_active or self.is_over:
            return
            
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        
        # Check timeout
        if elapsed >= self.time_limit:
            self.game_over(False)
            return
            
        # Update enemies
        for enemy in self.enemies:
            # Move patrol
            enemy["x"] += enemy["dir"] * 0.02
            
            # Check patrol range
            start_x = enemy["x"] - enemy["range"] // 2
            end_x = enemy["x"] + enemy["range"] // 2
            
            if int(enemy["x"]) <= max(1, int(start_x)) or int(enemy["x"]) >= min(self.map_width - 2, int(end_x) + 3):
                enemy["dir"] *= -1
                
            # Check player collision
            if int(enemy["x"]) == self.player_x and int(enemy.get("y", 0)) == self.player_y:
                self.take_damage()
                
    def move_player(self, dx, dy):
        """Move player"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        # Bounds check
        if new_x < 0 or new_x >= self.map_width or new_y < 0 or new_y >= self.map_height:
            return
            
        tile = self.map_data[new_y][new_x]
        
        # Wall
        if tile == '#':
            return
            
        # Locked door
        if tile == 'D':
            if self.has_key:
                self.map_data[new_y][new_x] = '.'
                self.has_key = False
            else:
                return
                
        # Move
        self.player_x = new_x
        self.player_y = new_y
        
        # Check tile effects
        tile = self.map_data[new_y][new_x]
        
        if tile == 'T':
            self.treasures_collected += 1
            self.map_data[new_y][new_x] = '.'
            
        elif tile == 'K':
            self.has_key = True
            self.map_data[new_y][new_x] = '.'
            
        elif tile == '^':
            self.take_damage()
            
        elif tile == 'E':
            if self.treasures_collected >= self.treasures_total:
                self.game_over(True)
                
    def take_damage(self):
        """Player takes damage"""
        self.player_hp -= 1
        if self.player_hp <= 0:
            self.game_over(False)
            
    def game_over(self, victory):
        """Handle game over"""
        self.is_over = True
        self.victory = victory
        
    def draw(self, background, ground):
        """Draw game"""
        self.screen.fill((30, 30, 40))
        
        # Draw map
        offset_y = 50
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size + offset_y, 
                                  self.tile_size, self.tile_size)
                
                if tile == '#':
                    pygame.draw.rect(self.screen, (60, 60, 70), rect)
                    pygame.draw.rect(self.screen, (80, 80, 90), rect, 1)
                elif tile == '.':
                    pygame.draw.rect(self.screen, (40, 45, 55), rect)
                elif tile == 'T':
                    pygame.draw.rect(self.screen, (40, 45, 55), rect)
                    # Treasure chest
                    pygame.draw.rect(self.screen, (139, 90, 43), 
                                   (rect.x + 8, rect.y + 12, 24, 18))
                    pygame.draw.rect(self.screen, (218, 165, 32), 
                                   (rect.x + 15, rect.y + 18, 10, 8))
                elif tile == 'K':
                    pygame.draw.rect(self.screen, (40, 45, 55), rect)
                    # Key
                    pygame.draw.circle(self.screen, (255, 215, 0), 
                                     (rect.centerx, rect.centery - 5), 8)
                    pygame.draw.rect(self.screen, (255, 215, 0), 
                                   (rect.centerx - 2, rect.centery, 4, 15))
                elif tile == '^':
                    pygame.draw.rect(self.screen, (40, 45, 55), rect)
                    # Spikes
                    for i in range(3):
                        spike_x = rect.x + 5 + i * 12
                        pygame.draw.polygon(self.screen, (150, 150, 160), [
                            (spike_x, rect.bottom - 5),
                            (spike_x + 10, rect.bottom - 5),
                            (spike_x + 5, rect.y + 10)
                        ])
                elif tile == 'D':
                    pygame.draw.rect(self.screen, (100, 70, 50), rect)
                    pygame.draw.rect(self.screen, (80, 50, 30), rect, 3)
                    # Lock
                    pygame.draw.circle(self.screen, (200, 200, 50), rect.center, 8)
                elif tile == 'E':
                    pygame.draw.rect(self.screen, (100, 255, 100), rect)
                    
        # Draw enemies
        for enemy in self.enemies:
            ex = int(enemy["x"]) * self.tile_size + self.tile_size // 2
            ey = enemy["y"] * self.tile_size + offset_y + self.tile_size // 2
            pygame.draw.circle(self.screen, (255, 80, 80), (ex, ey), 12)
            pygame.draw.circle(self.screen, WHITE, (ex + 3, ey - 2), 4)
            pygame.draw.circle(self.screen, BLACK, (ex + 4, ey - 2), 2)
            
        # Draw player
        px = self.player_x * self.tile_size + self.tile_size // 2
        py = self.player_y * self.tile_size + offset_y + self.tile_size // 2
        pygame.draw.circle(self.screen, (255, 220, 50), (px, py), 14)
        pygame.draw.circle(self.screen, WHITE, (px + 4, py - 2), 5)
        pygame.draw.circle(self.screen, BLACK, (px + 5, py - 2), 2)
        
        # HUD
        self.draw_hud()
        
        if self.is_over:
            self.draw_game_over()
            
    def draw_hud(self):
        """Draw HUD"""
        # Background bar
        pygame.draw.rect(self.screen, (50, 50, 60), (0, 0, SCREEN_WIDTH, 45))
        
        # HP
        for i in range(3):
            color = (255, 80, 80) if i < self.player_hp else (80, 80, 80)
            pygame.draw.circle(self.screen, color, (25 + i * 25, 22), 10)
            
        # Treasures
        treasure_text = f"Treasures: {self.treasures_collected}/{self.treasures_total}"
        treasure = self.font.render(treasure_text, True, COIN_COLOR)
        self.screen.blit(treasure, (100, 12))
        
        # Key indicator
        if self.has_key:
            key_text = self.font.render("KEY", True, (255, 215, 0))
            self.screen.blit(key_text, (260, 12))
            
        # Timer
        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        seconds = remaining // 1000
        
        timer_color = ACCENT_COLOR if seconds <= 20 else WHITE
        timer_text = self.font.render(f"Time: {seconds}s", True, timer_color)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 100, 12))
        
    def draw_game_over(self):
        """Draw game over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        if self.victory:
            title = self.big_font.render("TREASURE FOUND!", True, COIN_COLOR)
            elapsed = pygame.time.get_ticks() - self.start_time
            time_text = self.font.render(f"Time: {elapsed // 1000}s", True, WHITE)
        else:
            title = self.big_font.render("GAME OVER", True, ACCENT_COLOR)
            time_text = self.font.render(f"Treasures: {self.treasures_collected}/{self.treasures_total}", True, WHITE)
            
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 280))
        
        hint = self.font.render("Press SPACE to continue", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 350))
        
    def handle_event(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if self.is_over:
                if event.key == pygame.K_SPACE:
                    return "done"
            else:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.move_player(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.move_player(1, 0)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.move_player(0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.move_player(0, 1)
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over:
                return "done"
                
        return None
