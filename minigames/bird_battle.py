import pygame
import random
import math
from settings import *
from sprites.bird import Bird
from sprites.enemy import EnemyBird
from sprites.projectile import Bullet

class BirdBattle:
    """Enhanced PvP Bird Battle mini-game"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty
        
        # Game state
        self.is_active = False
        self.is_over = False
        self.winner = None
        self.round = 1
        self.max_rounds = 3
        self.player_wins = 0
        self.enemy_wins = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 24)
        
        # Sprites
        self.player = None
        self.enemy = None
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = []
        
        # Player stats
        self.player_hp = 3
        self.player_max_hp = 3
        
        # Shooting
        self.last_shot = 0
        self.shoot_cooldown = 400
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        
        # Special moves
        self.special_charge = 0
        self.special_max = 100
        self.special_ready = False
        
        # Power-up spawning
        self.last_powerup = 0
        self.powerup_interval = 4000
        
        # Round transition
        self.round_transition = False
        self.transition_timer = 0
        
        # Combo system
        self.combo = 0
        self.combo_timer = 0
        
        # Screen shake
        self.shake_amount = 0
        self.shake_offset = (0, 0)
        
    def start(self, skin_id="default"):
        """Start a new battle"""
        self.is_active = True
        self.is_over = False
        self.winner = None
        self.round = 1
        self.player_wins = 0
        self.enemy_wins = 0
        
        self.start_round(skin_id)
        
    def start_round(self, skin_id="default"):
        """Start a new round"""
        # Create player
        self.player = Bird(self.difficulty, skin_id)
        self.player.rect.x = 60
        self.player.rect.centery = SCREEN_HEIGHT // 2
        
        # Create enemy with difficulty scaling per round
        round_difficulty = ["easy", "medium", "hard"][min(self.round - 1, 2)]
        self.enemy = EnemyBird(round_difficulty)
        
        # Reset
        self.player_hp = self.player_max_hp
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.powerups.empty()
        self.particles.clear()
        
        self.last_shot = pygame.time.get_ticks()
        self.last_powerup = pygame.time.get_ticks()
        self.rapid_fire = False
        self.special_charge = 0
        self.special_ready = False
        self.combo = 0
        
        self.round_transition = True
        self.transition_timer = pygame.time.get_ticks()
        
    def update(self, dt):
        if not self.is_active or self.is_over:
            return
            
        now = pygame.time.get_ticks()
        
        # Round transition
        if self.round_transition:
            if now - self.transition_timer > 2000:
                self.round_transition = False
            return
        
        # Update screen shake
        if self.shake_amount > 0:
            self.shake_amount *= 0.85
            self.shake_offset = (
                random.randint(-int(self.shake_amount), int(self.shake_amount)),
                random.randint(-int(self.shake_amount), int(self.shake_amount))
            )
        else:
            self.shake_offset = (0, 0)
        
        # Update player
        if self.player and self.player.alive:
            self.player.update()
            
            # Bounds
            if self.player.rect.top < 0:
                self.player.rect.top = 0
            if self.player.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
                self.player.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                
        # Update enemy
        if self.enemy and self.enemy.alive:
            self.enemy.update(self.player, self.player_bullets)
            
            # Enemy shooting
            if self.enemy.can_shoot():
                bullet = self.enemy.shoot()
                self.enemy_bullets.add(bullet)
                
        # Update bullets
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.powerups.update()
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Combo timer
        if self.combo > 0 and now - self.combo_timer > 2000:
            self.combo = 0
        
        # Rapid fire timer
        if self.rapid_fire and now > self.rapid_fire_timer:
            self.rapid_fire = False
            self.shoot_cooldown = 400
            
        # Check collisions
        self.check_collisions()
        
        # Spawn powerups
        if now - self.last_powerup > self.powerup_interval:
            self.spawn_powerup()
            self.last_powerup = now
            
        # Check round end
        if self.player_hp <= 0:
            self.enemy_wins += 1
            self.check_match_end("player_lost")
        elif not self.enemy.alive:
            self.player_wins += 1
            # Bonus coins for winning rounds
            self.check_match_end("player_won")
            
    def check_collisions(self):
        """Check bullet collisions"""
        now = pygame.time.get_ticks()
        
        # Player bullets hitting enemy
        for bullet in list(self.player_bullets):
            if self.enemy and self.enemy.alive:
                if bullet.rect.colliderect(self.enemy.rect):
                    bullet.kill()
                    
                    # Combo
                    self.combo += 1
                    self.combo_timer = now
                    
                    # Damage with combo bonus
                    damage = 1 + (self.combo // 3)
                    killed = self.enemy.take_damage(damage)
                    
                    # Charge special
                    self.special_charge = min(self.special_max, self.special_charge + 15)
                    if self.special_charge >= self.special_max:
                        self.special_ready = True
                    
                    # Hit particles
                    self.spawn_hit_particles(bullet.rect.centerx, bullet.rect.centery, (255, 100, 100))
                    
                    # Screen shake on kill
                    if killed:
                        self.shake_amount = 15
                    else:
                        self.shake_amount = 5
                    
        # Enemy bullets hitting player
        for bullet in list(self.enemy_bullets):
            if self.player and self.player.alive:
                if bullet.rect.colliderect(self.player.rect):
                    bullet.kill()
                    
                    if not self.player.has_shield:
                        self.player_hp -= 1
                        self.shake_amount = 8
                        self.spawn_hit_particles(self.player.rect.centerx, self.player.rect.centery, (255, 255, 100))
                        self.combo = 0  # Reset combo on hit
                    else:
                        self.player.has_shield = False
                        self.spawn_hit_particles(self.player.rect.centerx, self.player.rect.centery, (100, 200, 255))
                        
        # Collect powerups
        for powerup in list(self.powerups):
            if self.player and self.player.rect.colliderect(powerup.rect):
                self.apply_powerup(powerup.powerup_type)
                powerup.kill()
                
    def spawn_hit_particles(self, x, y, color):
        """Spawn hit effect particles"""
        for _ in range(8):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            self.particles.append(HitParticle(x, y, angle, speed, color))
                
    def spawn_powerup(self):
        """Spawn a random powerup"""
        types = ["rapid", "shield", "heal", "special"]
        ptype = random.choice(types)
        
        x = SCREEN_WIDTH // 2 + random.randint(-50, 50)
        y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100)
        
        powerup = BattlePowerUp(x, y, ptype)
        self.powerups.add(powerup)
        
    def apply_powerup(self, ptype):
        """Apply powerup effect"""
        now = pygame.time.get_ticks()
        
        if ptype == "rapid":
            self.rapid_fire = True
            self.rapid_fire_timer = now + 6000
            self.shoot_cooldown = 150
        elif ptype == "shield":
            self.player.has_shield = True
            self.player.shield_timer = now + 15000
        elif ptype == "heal":
            self.player_hp = min(self.player_max_hp, self.player_hp + 1)
        elif ptype == "special":
            self.special_charge = self.special_max
            self.special_ready = True
            
    def use_special(self):
        """Use special attack"""
        if not self.special_ready:
            return
            
        self.special_ready = False
        self.special_charge = 0
        
        # Fire burst of bullets
        for angle in range(-30, 31, 10):
            rad = math.radians(angle)
            bullet = Bullet(
                self.player.rect.right,
                self.player.rect.centery,
                direction=1,
                speed=10,
                color=(255, 200, 50),
                owner="player"
            )
            bullet.vy = math.sin(rad) * 3
            self.player_bullets.add(bullet)
            
        self.shake_amount = 10
            
    def check_match_end(self, result):
        """Check if match is over"""
        if self.player_wins >= 2:
            self.is_over = True
            self.winner = "player"
        elif self.enemy_wins >= 2:
            self.is_over = True
            self.winner = "enemy"
        else:
            # Next round
            self.round += 1
            self.start_round(self.player.skin_id if self.player else "default")
            
    def player_jump(self):
        if self.player and self.player.alive and not self.round_transition:
            self.player.jump()
            
    def player_shoot(self):
        """Player shoots"""
        if self.round_transition:
            return False
            
        now = pygame.time.get_ticks()
        
        if now - self.last_shot >= self.shoot_cooldown:
            self.last_shot = now
            
            bullet = Bullet(
                self.player.rect.right,
                self.player.rect.centery,
                direction=1,
                color=(255, 255, 100),
                owner="player"
            )
            self.player_bullets.add(bullet)
            return True
        return False
        
    def draw(self, background, ground):
        """Draw battle scene"""
        # Apply screen shake
        offset = self.shake_offset
        
        # Background
        background.draw(self.screen)
        
        # Arena indicators
        pygame.draw.line(self.screen, (100, 100, 120, 50), 
                        (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - GROUND_HEIGHT), 2)
        
        # Powerups
        for powerup in self.powerups:
            pos = (powerup.rect.x + offset[0], powerup.rect.y + offset[1])
            self.screen.blit(powerup.image, pos)
            
        # Bullets
        for bullet in self.player_bullets:
            pos = (bullet.rect.x + offset[0], bullet.rect.y + offset[1])
            self.screen.blit(bullet.image, pos)
        for bullet in self.enemy_bullets:
            pos = (bullet.rect.x + offset[0], bullet.rect.y + offset[1])
            self.screen.blit(bullet.image, pos)
            
        # Particles
        for particle in self.particles:
            particle.draw(self.screen, offset)
            
        # Player
        if self.player:
            self.player.draw_effects(self.screen)
            pos = (self.player.rect.x + offset[0], self.player.rect.y + offset[1])
            self.screen.blit(self.player.image, pos)
            
        # Enemy
        if self.enemy and self.enemy.alive:
            pos = (self.enemy.rect.x + offset[0], self.enemy.rect.y + offset[1])
            self.screen.blit(self.enemy.image, pos)
            
        ground.draw(self.screen)
        
        # HUD
        self.draw_hud()
        
        # Round transition
        if self.round_transition:
            self.draw_round_transition()
        
        # Game over overlay
        if self.is_over:
            self.draw_game_over()
            
    def draw_hud(self):
        """Draw battle HUD"""
        # Player HP (hearts)
        for i in range(self.player_max_hp):
            x = 20 + i * 40
            y = 20
            color = (255, 80, 80) if i < self.player_hp else (80, 80, 80)
            # Heart shape
            pygame.draw.circle(self.screen, color, (x + 10, y + 8), 10)
            pygame.draw.circle(self.screen, color, (x + 22, y + 8), 10)
            pygame.draw.polygon(self.screen, color, [
                (x + 2, y + 12), (x + 16, y + 28), (x + 30, y + 12)
            ])
            
        # Enemy HP
        if self.enemy:
            for i in range(self.enemy.max_hp):
                x = SCREEN_WIDTH - 130 + i * 40
                y = 20
                color = (255, 80, 80) if i < self.enemy.hp else (80, 80, 80)
                pygame.draw.circle(self.screen, color, (x + 10, y + 8), 10)
                pygame.draw.circle(self.screen, color, (x + 22, y + 8), 10)
                pygame.draw.polygon(self.screen, color, [
                    (x + 2, y + 12), (x + 16, y + 28), (x + 30, y + 12)
                ])
                
        # Round indicator
        round_text = self.font.render(f"Round {self.round}", True, WHITE)
        self.screen.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, 15))
        
        # Score
        score_text = self.small_font.render(f"{self.player_wins} - {self.enemy_wins}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 45))
        
        # Combo
        if self.combo >= 2:
            combo_text = self.font.render(f"COMBO x{self.combo}!", True, (255, 200, 50))
            self.screen.blit(combo_text, (20, 60))
            
        # Special meter
        meter_width = 120
        meter_x = 20
        meter_y = SCREEN_HEIGHT - 50
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 60), (meter_x, meter_y, meter_width, 20), border_radius=5)
        
        # Fill
        fill_width = int(meter_width * (self.special_charge / self.special_max))
        fill_color = (255, 200, 50) if self.special_ready else (100, 150, 255)
        pygame.draw.rect(self.screen, fill_color, (meter_x, meter_y, fill_width, 20), border_radius=5)
        
        # Border
        pygame.draw.rect(self.screen, (100, 100, 110), (meter_x, meter_y, meter_width, 20), 2, border_radius=5)
        
        # Label
        special_label = "SPECIAL READY!" if self.special_ready else "SPECIAL"
        label_color = (255, 200, 50) if self.special_ready else WHITE
        label = self.small_font.render(special_label, True, label_color)
        self.screen.blit(label, (meter_x + meter_width + 10, meter_y + 2))
        
        # Rapid fire indicator
        if self.rapid_fire:
            rapid = self.small_font.render("RAPID FIRE!", True, (255, 150, 50))
            self.screen.blit(rapid, (20, 90))
            
        # Controls hint
        controls = self.small_font.render("SPACE: Jump | X: Shoot | C: Special", True, (150, 150, 160))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 25))
        
    def draw_round_transition(self):
        """Draw round start screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        round_text = self.big_font.render(f"ROUND {self.round}", True, WHITE)
        self.screen.blit(round_text, (SCREEN_WIDTH // 2 - round_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        
        fight_text = self.font.render("GET READY!", True, ACCENT_COLOR)
        self.screen.blit(fight_text, (SCREEN_WIDTH // 2 - fight_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        if self.winner == "player":
            text = "VICTORY!"
            color = (100, 255, 100)
            subtext = f"You won {self.player_wins}-{self.enemy_wins}!"
        else:
            text = "DEFEAT"
            color = (255, 100, 100)
            subtext = f"Enemy won {self.enemy_wins}-{self.player_wins}"
            
        title = self.big_font.render(text, True, color)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
        
        sub = self.font.render(subtext, True, WHITE)
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 260))
        
        hint = self.font.render("Press SPACE to continue", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 340))
        
    def handle_event(self, event):
        """Handle battle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.is_over:
                    return "done"
                else:
                    self.player_jump()
            elif event.key == pygame.K_x:
                self.player_shoot()
            elif event.key == pygame.K_c:
                self.use_special()
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.is_over:
                    return "done"
                else:
                    self.player_jump()
            elif event.button == 3:  # Right click
                self.player_shoot()
                
        return None


class HitParticle:
    """Particle for hit effects"""
    
    def __init__(self, x, y, angle, speed, color):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = 1.0
        self.size = random.randint(3, 6)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15  # Gravity
        self.life -= 0.05
        return self.life > 0
        
    def draw(self, screen, offset=(0, 0)):
        if self.life > 0:
            alpha = int(255 * self.life)
            size = int(self.size * self.life)
            if size > 0:
                pygame.draw.circle(screen, self.color, 
                                 (int(self.x + offset[0]), int(self.y + offset[1])), size)


class BattlePowerUp(pygame.sprite.Sprite):
    """Power-up for Bird Battle"""
    
    def __init__(self, x, y, powerup_type):
        super().__init__()
        
        self.powerup_type = powerup_type
        self.create_sprite()
        
        self.rect = self.image.get_rect(center=(x, y))
        self.base_y = y
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10000
        
    def create_sprite(self):
        size = 36
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        colors = {
            "rapid": (255, 150, 50),
            "shield": (100, 200, 255),
            "heal": (100, 255, 100),
            "special": (255, 200, 50)
        }
        color = colors.get(self.powerup_type, (200, 200, 200))
        
        # Outer glow
        pygame.draw.circle(self.image, (*color, 80), (size // 2, size // 2), size // 2)
        
        # Main circle
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2 - 4)
        pygame.draw.circle(self.image, WHITE, (size // 2, size // 2), size // 2 - 4, 2)
        
        # Icon
        center = size // 2
        if self.powerup_type == "rapid":
            # Double arrows
            pygame.draw.polygon(self.image, WHITE, [
                (center - 6, center - 4), (center + 4, center), (center - 6, center + 4)
            ])
            pygame.draw.polygon(self.image, WHITE, [
                (center - 2, center - 4), (center + 8, center), (center - 2, center + 4)
            ])
        elif self.powerup_type == "shield":
            # Shield
            pygame.draw.polygon(self.image, WHITE, [
                (center, center - 8), (center + 8, center - 4),
                (center + 6, center + 6), (center, center + 10),
                (center - 6, center + 6), (center - 8, center - 4)
            ], 2)
        elif self.powerup_type == "heal":
            # Plus
            pygame.draw.rect(self.image, WHITE, (center - 2, center - 8, 4, 16))
            pygame.draw.rect(self.image, WHITE, (center - 8, center - 2, 16, 4))
        elif self.powerup_type == "special":
            # Star
            points = []
            for i in range(5):
                angle = math.radians(-90 + i * 72)
                points.append((center + int(8 * math.cos(angle)), center + int(8 * math.sin(angle))))
                angle = math.radians(-90 + i * 72 + 36)
                points.append((center + int(4 * math.cos(angle)), center + int(4 * math.sin(angle))))
            pygame.draw.polygon(self.image, WHITE, points)
            
    def update(self):
        now = pygame.time.get_ticks()
        
        # Float animation
        self.rect.centery = int(self.base_y + math.sin(now / 200) * 10)
        
        # Pulse effect
        scale = 1.0 + math.sin(now / 150) * 0.1
        
        # Expire
        if now - self.spawn_time > self.lifetime:
            self.kill()
