import pygame
import random
import math
from settings import *
from sprites.projectile import Bullet

class EnemyBird(pygame.sprite.Sprite):
    """AI-controlled enemy bird for Bird Battle"""
    
    def __init__(self, difficulty="medium", x=None, y=None):
        super().__init__()
        
        self.difficulty = difficulty
        self.create_sprite()
        
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = x if x else SCREEN_WIDTH - 100
        self.rect.centery = y if y else SCREEN_HEIGHT // 2
        
        # Stats
        self.hp = 3
        self.max_hp = 3
        self.alive = True
        
        # Physics
        self.velocity = 0
        self.gravity = 0.25
        self.jump_power = -5
        
        # AI behavior
        self.ai_settings = self.get_ai_settings()
        self.last_shot = 0
        self.last_decision = 0
        self.target_y = self.rect.centery
        
        # Animation
        self.angle = 0
        self.hit_flash = 0
        
    def get_ai_settings(self):
        settings = {
            "easy": {
                "accuracy": 0.4,
                "reaction_time": 800,
                "shoot_cooldown": 1500,
                "dodge_chance": 0.3
            },
            "medium": {
                "accuracy": 0.6,
                "reaction_time": 500,
                "shoot_cooldown": 1000,
                "dodge_chance": 0.5
            },
            "hard": {
                "accuracy": 0.85,
                "reaction_time": 250,
                "shoot_cooldown": 700,
                "dodge_chance": 0.7
            }
        }
        return settings.get(self.difficulty, settings["medium"])
        
    def create_sprite(self):
        """Create enemy bird sprite - red colored"""
        self.base_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
        
        center_x, center_y = BIRD_WIDTH // 2, BIRD_HEIGHT // 2
        
        # Body (red)
        pygame.draw.ellipse(self.base_image, (220, 60, 60), (2, 3, BIRD_WIDTH - 8, BIRD_HEIGHT - 6))
        pygame.draw.ellipse(self.base_image, (180, 40, 40), (2, 3, BIRD_WIDTH - 8, BIRD_HEIGHT - 6), 2)
        
        # Wing
        pygame.draw.ellipse(self.base_image, (200, 50, 50), (BIRD_WIDTH - 20, center_y - 1, 14, 12))
        
        # Eye
        pygame.draw.circle(self.base_image, WHITE, (center_x - 6, center_y - 4), 7)
        pygame.draw.circle(self.base_image, BLACK, (center_x - 8, center_y - 4), 4)
        pygame.draw.circle(self.base_image, WHITE, (center_x - 6, center_y - 6), 2)
        
        # Beak (pointing left)
        pygame.draw.polygon(self.base_image, (255, 140, 50), [
            (8, center_y), (0, center_y + 3), (8, center_y + 6)
        ])
        
        self.image = self.base_image.copy()
        
    def update(self, player_bird=None, bullets=None):
        if not self.alive:
            return
            
        now = pygame.time.get_ticks()
        
        # Update hit flash
        if self.hit_flash > 0:
            self.hit_flash -= 1
            
        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)
        
        # AI decision making
        if now - self.last_decision > self.ai_settings["reaction_time"]:
            self.last_decision = now
            self.make_decision(player_bird, bullets)
            
        # Move towards target
        if self.rect.centery < self.target_y - 20:
            pass  # Fall naturally
        elif self.rect.centery > self.target_y + 20:
            self.jump()
            
        # Keep in bounds
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.velocity = 0
            
        # Update sprite rotation
        self.target_angle = -self.velocity * 3
        self.target_angle = max(-90, min(25, self.target_angle))
        self.angle += (self.target_angle - self.angle) * 0.2
        
        # Apply rotation and flash
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        if self.hit_flash > 0 and self.hit_flash % 4 < 2:
            # Flash white
            flash_surf = self.image.copy()
            flash_surf.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_ADD)
            self.image = flash_surf
            
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
    def make_decision(self, player_bird, bullets):
        """AI decision making"""
        if not player_bird:
            return
            
        # Dodge bullets
        if bullets and random.random() < self.ai_settings["dodge_chance"]:
            for bullet in bullets:
                if bullet.owner == "player":
                    # Check if bullet is heading towards us
                    if bullet.rect.right > self.rect.left - 100 and bullet.rect.left < self.rect.right:
                        if abs(bullet.rect.centery - self.rect.centery) < 50:
                            # Dodge!
                            if bullet.rect.centery < self.rect.centery:
                                self.target_y = self.rect.centery + 80
                            else:
                                self.target_y = self.rect.centery - 80
                            return
        
        # Track player with some randomness
        if random.random() < self.ai_settings["accuracy"]:
            self.target_y = player_bird.rect.centery + random.randint(-30, 30)
        else:
            self.target_y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100)
            
    def jump(self):
        if self.alive:
            self.velocity = self.jump_power
            
    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.ai_settings["shoot_cooldown"]:
            if random.random() < self.ai_settings["accuracy"]:
                self.last_shot = now
                return True
        return False
        
    def shoot(self):
        """Create bullet going left"""
        return Bullet(
            self.rect.left, 
            self.rect.centery,
            direction=-1,
            color=(255, 100, 100),
            owner="enemy"
        )
        
    def take_damage(self, amount=1):
        self.hp -= amount
        self.hit_flash = 20
        
        if self.hp <= 0:
            self.alive = False
            return True
        return False
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Boss(pygame.sprite.Sprite):
    """Boss enemy for Boss Rush mode"""
    
    def __init__(self):
        super().__init__()
        
        self.max_hp = 100
        self.hp = self.max_hp
        self.phase = 1
        self.alive = True
        
        self.create_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.right = SCREEN_WIDTH + 50
        self.rect.centery = SCREEN_HEIGHT // 2
        
        # State
        self.state = "entering"  # entering, idle, attacking, vulnerable
        self.state_timer = 0
        self.attack_pattern = 0
        
        # Movement
        self.base_x = SCREEN_WIDTH - 120
        self.target_y = SCREEN_HEIGHT // 2
        self.move_speed = 2
        
        # Attack timers
        self.last_attack = 0
        self.attack_cooldown = 2000
        
        # Visual
        self.hit_flash = 0
        self.weak_point_glow = 0
        
    def create_sprite(self):
        """Create boss sprite - giant raven"""
        size = 100
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Body
        pygame.draw.ellipse(self.image, (30, 30, 40), (10, 20, 80, 60))
        pygame.draw.ellipse(self.image, (20, 20, 30), (10, 20, 80, 60), 3)
        
        # Wing (left)
        wing_points = [(5, 50), (0, 30), (15, 45), (10, 60), (0, 70)]
        pygame.draw.polygon(self.image, (40, 40, 50), wing_points)
        
        # Head
        pygame.draw.circle(self.image, (35, 35, 45), (75, 35), 22)
        
        # Eye - weak point in phase 1
        eye_color = (255, 50, 50) if self.phase == 1 else (200, 50, 50)
        pygame.draw.circle(self.image, eye_color, (82, 32), 8)
        pygame.draw.circle(self.image, (255, 100, 100), (80, 30), 3)
        
        # Beak
        pygame.draw.polygon(self.image, (60, 50, 40), [
            (95, 38), (100, 42), (95, 46), (88, 42)
        ])
        
        # Chest weak point - phase 2
        if self.phase >= 2:
            chest_color = (255, 150, 50) if self.phase == 2 else (150, 100, 50)
            pygame.draw.circle(self.image, chest_color, (50, 50), 12)
            
        # Wing weak points - phase 3
        if self.phase == 3:
            pygame.draw.circle(self.image, (100, 255, 100), (8, 50), 8)
            
    def update(self, dt=0):
        if not self.alive:
            return
            
        now = pygame.time.get_ticks()
        
        # Update timers
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.weak_point_glow = (self.weak_point_glow + 5) % 360
        
        # State machine
        if self.state == "entering":
            # Move onto screen
            if self.rect.right > self.base_x + 60:
                self.rect.x -= 3
            else:
                self.state = "idle"
                self.state_timer = now
                
        elif self.state == "idle":
            # Float up and down
            self.target_y = SCREEN_HEIGHT // 2 + math.sin(now / 500) * 50
            self.rect.centery += (self.target_y - self.rect.centery) * 0.05
            
            # Decide to attack
            if now - self.state_timer > 2000:
                self.state = "attacking"
                self.attack_pattern = random.randint(0, 2)
                self.state_timer = now
                
        elif self.state == "attacking":
            # Attack duration
            if now - self.state_timer > 1500:
                self.state = "vulnerable"
                self.state_timer = now
                
        elif self.state == "vulnerable":
            # Brief vulnerable window
            if now - self.state_timer > 1500:
                self.state = "idle"
                self.state_timer = now
                
        # Update phase based on HP
        if self.hp <= self.max_hp * 0.33:
            if self.phase < 3:
                self.phase = 3
                self.create_sprite()
        elif self.hp <= self.max_hp * 0.66:
            if self.phase < 2:
                self.phase = 2
                self.create_sprite()
                
    def get_attack(self):
        """Get current attack pattern bullets/lasers"""
        attacks = []
        
        if self.state != "attacking":
            return attacks
            
        if self.phase == 1:
            # Phase 1: 3 bullets straight
            if self.attack_pattern == 0:
                for offset in [-20, 0, 20]:
                    attacks.append(Bullet(
                        self.rect.left, self.rect.centery + offset,
                        direction=-1, speed=6, color=(150, 50, 150), owner="boss"
                    ))
                    
        elif self.phase == 2:
            # Phase 2: Spread shot
            if self.attack_pattern == 0:
                for angle in range(-30, 31, 15):
                    rad = math.radians(180 + angle)
                    attacks.append(Bullet(
                        self.rect.left, self.rect.centery,
                        direction=-1, speed=5, color=(255, 150, 50), owner="boss"
                    ))
                    
        elif self.phase == 3:
            # Phase 3: More bullets + summon
            for angle in range(-40, 41, 20):
                attacks.append(Bullet(
                    self.rect.left, self.rect.centery,
                    direction=-1, speed=7, color=(100, 255, 100), owner="boss"
                ))
                
        return attacks
        
    def take_damage(self, amount=1, hit_weak_point=False):
        if hit_weak_point and self.state == "vulnerable":
            amount *= 2
            
        self.hp -= amount
        self.hit_flash = 15
        
        if self.hp <= 0:
            self.alive = False
            return True
        return False
        
    def get_weak_point_rect(self):
        """Get current weak point hitbox"""
        if self.phase == 1:
            # Eye
            return pygame.Rect(self.rect.x + 74, self.rect.y + 24, 16, 16)
        elif self.phase == 2:
            # Chest
            return pygame.Rect(self.rect.x + 38, self.rect.y + 38, 24, 24)
        else:
            # Wing
            return pygame.Rect(self.rect.x, self.rect.y + 42, 16, 16)
            
    def draw_hp_bar(self, screen):
        """Draw boss HP bar at top"""
        bar_width = 300
        bar_height = 20
        x = (SCREEN_WIDTH - bar_width) // 2
        y = 20
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (x - 2, y - 2, bar_width + 4, bar_height + 4), border_radius=5)
        
        # HP fill
        hp_ratio = self.hp / self.max_hp
        fill_width = int(bar_width * hp_ratio)
        
        # Color based on phase
        colors = {1: (255, 50, 50), 2: (255, 150, 50), 3: (100, 255, 100)}
        color = colors.get(self.phase, (255, 50, 50))
        
        pygame.draw.rect(screen, color, (x, y, fill_width, bar_height), border_radius=3)
        
        # Phase markers
        for i in range(1, 3):
            marker_x = x + int(bar_width * (1 - i * 0.33))
            pygame.draw.line(screen, WHITE, (marker_x, y), (marker_x, y + bar_height), 2)
            
        # Boss name
        font = pygame.font.Font(None, 24)
        name = font.render("THE GIANT RAVEN", True, WHITE)
        screen.blit(name, (SCREEN_WIDTH // 2 - name.get_width() // 2, y + bar_height + 5))
