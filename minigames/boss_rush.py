from settings import get_vn_font
import pygame
import random
from settings import *
from sprites.bird import Bird
from sprites.enemy import Boss
from sprites.projectile import Bullet

class BossRush:
    """Boss Rush mini-game - fight the Giant Raven"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty
        
        # Game state
        self.is_active = False
        self.is_over = False
        self.victory = False
        self.hits_taken = 0
        
        # Fonts
        self.font = get_vn_font(36)
        self.big_font = get_vn_font(72)
        
        # Sprites
        self.player = None
        self.boss = None
        self.player_bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        
        # Shooting
        self.last_shot = 0
        self.shoot_cooldown = 300
        
        # Boss attack timer
        self.last_boss_attack = 0
        self.boss_attack_cooldown = 2000
        
    def start(self, skin_id="default"):
        """Start boss fight"""
        self.is_active = True
        self.is_over = False
        self.victory = False
        self.hits_taken = 0
        
        # Create player
        self.player = Bird(self.difficulty, skin_id)
        self.player.rect.x = 80
        self.player.rect.centery = SCREEN_HEIGHT // 2
        
        # Create boss
        self.boss = Boss()
        
        # Clear bullets
        self.player_bullets.empty()
        self.boss_bullets.empty()
        
        self.last_shot = pygame.time.get_ticks()
        self.last_boss_attack = pygame.time.get_ticks()
        
    def update(self, dt):
        if not self.is_active or self.is_over:
            return
            
        now = pygame.time.get_ticks()
        
        # Update player
        if self.player and self.player.alive:
            self.player.update()
            
            # Bounds
            if self.player.rect.top < 0:
                self.player.rect.top = 0
            if self.player.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
                self.player.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            if self.player.rect.left < 0:
                self.player.rect.left = 0
            if self.player.rect.right > SCREEN_WIDTH // 2:
                self.player.rect.right = SCREEN_WIDTH // 2
                
        # Update boss
        if self.boss and self.boss.alive:
            self.boss.update(dt)
            
            # Boss attacks
            if now - self.last_boss_attack > self.boss_attack_cooldown:
                self.last_boss_attack = now
                attacks = self.boss.get_attack()
                for bullet in attacks:
                    self.boss_bullets.add(bullet)
                    
        # Update bullets
        self.player_bullets.update()
        self.boss_bullets.update()
        
        # Check collisions
        self.check_collisions()
        
        # Check win/lose
        if self.boss and not self.boss.alive:
            self.is_over = True
            self.victory = True
        elif self.player and not self.player.alive:
            self.is_over = True
            self.victory = False
            
    def check_collisions(self):
        """Check bullet collisions"""
        # Player bullets hitting boss
        for bullet in list(self.player_bullets):
            if self.boss and self.boss.alive:
                weak_rect = self.boss.get_weak_point_rect()
                
                if bullet.rect.colliderect(weak_rect):
                    bullet.kill()
                    self.boss.take_damage(5, hit_weak_point=True)
                elif bullet.rect.colliderect(self.boss.rect):
                    bullet.kill()
                    self.boss.take_damage(1)
                    
        # Boss bullets hitting player
        for bullet in list(self.boss_bullets):
            if self.player and self.player.alive:
                if bullet.rect.colliderect(self.player.rect):
                    bullet.kill()
                    self.hits_taken += 1
                    
                    if self.hits_taken >= 5:  # 5 hits = death
                        self.player.alive = False
                        
    def player_shoot(self):
        """Player shoots"""
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
            
    def draw(self, background, ground):
        """Draw boss fight"""
        background.draw(self.screen)
        
        # Bullets
        for bullet in self.player_bullets:
            self.screen.blit(bullet.image, bullet.rect)
        for bullet in self.boss_bullets:
            self.screen.blit(bullet.image, bullet.rect)
            
        # Boss
        if self.boss and self.boss.alive:
            self.screen.blit(self.boss.image, self.boss.rect)
            
            # Draw weak point indicator when vulnerable
            if self.boss.state == "vulnerable":
                weak_rect = self.boss.get_weak_point_rect()
                pygame.draw.rect(self.screen, (255, 255, 0), weak_rect, 2)
                
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
        # Boss HP bar
        if self.boss and self.boss.alive:
            self.boss.draw_hp_bar(self.screen)
            
        # Player HP
        hp = 5 - self.hits_taken
        for i in range(5):
            x = 20 + i * 25
            y = SCREEN_HEIGHT - 50
            color = (255, 80, 80) if i < hp else (80, 80, 80)
            pygame.draw.circle(self.screen, color, (x + 10, y + 10), 10)
            
        # Phase indicator
        if self.boss:
            phase = self.font.render(f"Phase {self.boss.phase}", True, PRIMARY_COLOR)
            self.screen.blit(phase, (20, 60))
            
        # Controls
        ctrl = get_vn_font(20).render("SPACE: Jump | X: Shoot", True, (180, 180, 180))
        self.screen.blit(ctrl, (SCREEN_WIDTH // 2 - ctrl.get_width() // 2, SCREEN_HEIGHT - 25))
        
    def draw_game_over(self):
        """Draw game over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        if self.victory:
            title = self.big_font.render("VICTORY!", True, (100, 255, 100))
            
            # Rank
            if self.hits_taken == 0:
                rank = "S"
                rank_color = (255, 215, 0)
                reward = 200
            elif self.hits_taken <= 2:
                rank = "A"
                rank_color = (200, 200, 200)
                reward = 100
            elif self.hits_taken <= 4:
                rank = "B"
                rank_color = (205, 127, 50)
                reward = 50
            else:
                rank = "C"
                rank_color = (150, 150, 150)
                reward = 25
                
            rank_text = self.big_font.render(f"Rank: {rank}", True, rank_color)
            reward_text = self.font.render(f"+{reward} coins!", True, COIN_COLOR)
        else:
            title = self.big_font.render("DEFEATED", True, ACCENT_COLOR)
            rank_text = None
            reward_text = None
            
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        if rank_text:
            self.screen.blit(rank_text, (SCREEN_WIDTH // 2 - rank_text.get_width() // 2, 240))
        if reward_text:
            self.screen.blit(reward_text, (SCREEN_WIDTH // 2 - reward_text.get_width() // 2, 320))
            
        hint = self.font.render("Press SPACE to continue", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 400))
        
    def handle_event(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.is_over:
                    return "done"
                elif self.player and self.player.alive:
                    self.player.jump()
            elif event.key == pygame.K_x:
                if self.player and self.player.alive:
                    self.player_shoot()
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_over:
                    return "done"
                elif self.player and self.player.alive:
                    self.player.jump()
            elif event.button == 3:
                if self.player and self.player.alive:
                    self.player_shoot()
                    
        return None

