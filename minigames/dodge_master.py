import pygame
import random
import math
from settings import *
from sprites.bird import Bird
from sprites.projectile import FallingObstacle, Laser, BombFragment

class DodgeMaster:
    """Dodge Master survival mini-game"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty
        
        # Game state
        self.is_active = False
        self.is_over = False
        self.score = 0
        self.wave = 1
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Sprites
        self.player = None
        self.obstacles = pygame.sprite.Group()
        self.fragments = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        
        # Timing
        self.start_time = 0
        self.last_spawn = 0
        self.spawn_rate = 1000  # ms between spawns
        self.last_wave = 0
        self.wave_duration = 30000  # 30 seconds per wave
        
        # Dash
        self.dash_ready = True
        self.dash_cooldown = 3000
        self.last_dash = 0
        
        # Movement
        self.move_left = False
        self.move_right = False
        self.move_speed = 5
        
    def start(self, skin_id="default"):
        """Start new game"""
        self.is_active = True
        self.is_over = False
        self.score = 0
        self.wave = 1
        
        # Create player
        self.player = Bird(self.difficulty, skin_id)
        self.player.rect.centerx = SCREEN_WIDTH // 2
        self.player.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT - 20
        self.player.gravity = 0  # No gravity in this mode
        
        # Clear obstacles
        self.obstacles.empty()
        self.fragments.empty()
        self.lasers.empty()
        
        # Start timers
        self.start_time = pygame.time.get_ticks()
        self.last_spawn = self.start_time
        self.last_wave = self.start_time
        
        self.dash_ready = True
        self.move_left = False
        self.move_right = False
        
    def update(self, dt):
        if not self.is_active or self.is_over:
            return
            
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        
        # Update score (survival time)
        self.score = elapsed // 100
        
        # Wave progression
        if now - self.last_wave > self.wave_duration:
            self.wave += 1
            self.last_wave = now
            self.spawn_rate = max(300, self.spawn_rate - 100)
            
        # Player movement
        if self.player and self.player.alive:
            if self.move_left:
                self.player.rect.x -= self.move_speed
            if self.move_right:
                self.player.rect.x += self.move_speed
                
            # Keep in bounds
            self.player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
            
        # Spawn obstacles
        if now - self.last_spawn > self.spawn_rate:
            self.spawn_obstacle()
            self.last_spawn = now
            
        # Boss waves - lasers
        if self.wave >= 5 and self.wave % 5 == 0:
            if random.random() < 0.01:  # 1% chance per frame
                self.spawn_laser()
                
        # Update obstacles
        self.obstacles.update()
        self.fragments.update()
        self.lasers.update()
        
        # Check bomb explosions
        self.check_bomb_explosions()
        
        # Check collisions
        self.check_collisions()
        
        # Dash cooldown
        if not self.dash_ready and now - self.last_dash > self.dash_cooldown:
            self.dash_ready = True
            
    def spawn_obstacle(self):
        """Spawn random obstacle"""
        x = random.randint(30, SCREEN_WIDTH - 30)
        
        # Obstacle type based on wave
        if self.wave < 3:
            types = ["rock"]
        elif self.wave < 5:
            types = ["rock", "rock", "missile"]
        elif self.wave < 8:
            types = ["rock", "missile", "bomb"]
        else:
            types = ["rock", "missile", "missile", "bomb"]
            
        obstacle_type = random.choice(types)
        
        # Speed increases with wave
        speed = 3 + self.wave * 0.5
        
        obstacle = FallingObstacle(x, obstacle_type, speed)
        self.obstacles.add(obstacle)
        
        # Missiles move horizontally
        if obstacle_type == "missile":
            obstacle.horizontal = True
            obstacle.hspeed = random.choice([-3, 3])
            obstacle.rect.left = 0 if obstacle.hspeed > 0 else SCREEN_WIDTH
            obstacle.rect.centery = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100)
            
    def spawn_laser(self):
        """Spawn horizontal laser"""
        y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
        laser = Laser(y)
        self.lasers.add(laser)
        
    def check_bomb_explosions(self):
        """Check for bomb explosions at ground level"""
        for obstacle in list(self.obstacles):
            if obstacle.obstacle_type == "bomb":
                if obstacle.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT - 10:
                    # Explode!
                    cx, cy = obstacle.rect.center
                    for angle in range(0, 360, 30):
                        frag = BombFragment(cx, cy, angle)
                        self.fragments.add(frag)
                    obstacle.kill()
                    
    def check_collisions(self):
        """Check player collisions"""
        if not self.player or not self.player.alive:
            return
            
        # Obstacles
        for obstacle in self.obstacles:
            # Skip missiles that are just moving horizontally
            if hasattr(obstacle, 'horizontal') and obstacle.horizontal:
                if obstacle.rect.colliderect(self.player.rect):
                    self.game_over()
                    return
            elif obstacle.rect.colliderect(self.player.rect):
                self.game_over()
                return
                
        # Fragments
        for frag in self.fragments:
            if frag.rect.colliderect(self.player.rect):
                self.game_over()
                return
                
        # Lasers (only when active)
        for laser in self.lasers:
            if laser.is_active and laser.rect.colliderect(self.player.rect):
                self.game_over()
                return
                
    def dash(self, direction):
        """Perform dash move"""
        if not self.dash_ready or not self.player:
            return False
            
        now = pygame.time.get_ticks()
        
        dash_distance = 80
        if direction == "left":
            self.player.rect.x -= dash_distance
        else:
            self.player.rect.x += dash_distance
            
        # Keep in bounds
        self.player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.dash_ready = False
        self.last_dash = now
        
        return True
        
    def game_over(self):
        """Handle game over"""
        self.is_over = True
        if self.player:
            self.player.alive = False
            
    def draw(self, background, ground):
        """Draw game"""
        background.draw(self.screen)
        
        # Obstacles
        for obstacle in self.obstacles:
            self.screen.blit(obstacle.image, obstacle.rect)
            
        # Lasers
        for laser in self.lasers:
            self.screen.blit(laser.image, laser.rect)
            
        # Fragments
        for frag in self.fragments:
            self.screen.blit(frag.image, frag.rect)
            
        ground.draw(self.screen)
        
        # Player
        if self.player:
            self.screen.blit(self.player.image, self.player.rect)
            
        # HUD
        self.draw_hud()
        
        if self.is_over:
            self.draw_game_over()
            
    def draw_hud(self):
        """Draw HUD"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Wave
        wave_text = self.font.render(f"Wave {self.wave}", True, PRIMARY_COLOR)
        self.screen.blit(wave_text, (SCREEN_WIDTH - 120, 20))
        
        # Dash indicator
        if self.dash_ready:
            dash_text = pygame.font.Font(None, 24).render("DASH READY [SPACE]", True, (100, 255, 100))
        else:
            remaining = max(0, self.dash_cooldown - (pygame.time.get_ticks() - self.last_dash))
            dash_text = pygame.font.Font(None, 24).render(f"Dash: {remaining // 1000 + 1}s", True, (150, 150, 150))
        self.screen.blit(dash_text, (SCREEN_WIDTH // 2 - dash_text.get_width() // 2, SCREEN_HEIGHT - 30))
        
        # Controls hint
        hint = pygame.font.Font(None, 20).render("← → to move", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
        
    def draw_game_over(self):
        """Draw game over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        title = self.big_font.render("GAME OVER", True, ACCENT_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
        
        score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, 270))
        
        wave = self.font.render(f"Reached Wave: {self.wave}", True, PRIMARY_COLOR)
        self.screen.blit(wave, (SCREEN_WIDTH // 2 - wave.get_width() // 2, 310))
        
        hint = self.font.render("Press SPACE to continue", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 380))
        
    def handle_event(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.is_over:
                    return "done"
                    
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_left = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_right = True
            elif event.key == pygame.K_SPACE and not self.is_over:
                # Dash in current direction
                if self.move_left:
                    self.dash("left")
                elif self.move_right:
                    self.dash("right")
                    
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_left = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_right = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over:
                return "done"
                
        return None
