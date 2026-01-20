import pygame
import sys
import random
import math
import asyncio
from settings import *
from sprites.bird import Bird
from sprites.pipe import Pipe
from sprites.background import Background, Ground
from sprites.particles import ParticleSystem
from sprites.collectibles import Coin, PowerUp
from managers.score_manager import ScoreManager, GameDataManager
from ui.menus import MainMenu, SettingsMenu, GameOverScreen, PauseScreen
from ui.shop import ShopMenu
from ui.minigames import MiniGameMenu, TimeAttackMode, ZenMode, DailyChallenge
from ui.components import ScoreDisplay

# Import new mini-games
from minigames.bird_battle import BirdBattle
from minigames.dodge_master import DodgeMaster
from minigames.memory_flight import MemoryFlight
from minigames.boss_rush import BossRush
from minigames.treasure_hunt import TreasureHunt

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # State
        self.state = STATE_MENU
        self.running = True
        self.difficulty = "medium"
        self.dt = 0
        self.game_mode = "classic"
        
        # Managers
        self.score_manager = ScoreManager()
        self.game_data = GameDataManager()
        self.particle_system = ParticleSystem()
        
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Background
        self.background = Background(self.difficulty)
        self.ground = Ground(self.difficulty)
        
        # Bird
        self.bird = None
        
        # UI
        self.init_ui()
        
        # Mini-games
        self.init_minigames()
        
        # HUD
        self.score_display = ScoreDisplay(SCREEN_WIDTH // 2, 50)
        self.hud_font = pygame.font.Font(None, 28)
        
        # Timers
        self.last_pipe_spawn = 0
        self.last_coin_spawn = 0
        
        # Session
        self.coins_this_game = 0
        self.combo_count = 0
        self.score_multiplier = 1.0
        
        # Power-ups
        self.has_coin_magnet = False
        self.magnet_timer = 0
        self.has_slow_motion = False
        self.slow_timer = 0
        self.has_score_boost = False
        self.score_boost_timer = 0
        
        # Get ready
        self.get_ready = False
        self.get_ready_timer = 0
        
    def init_ui(self):
        self.main_menu = MainMenu(self.screen, self.score_manager.get_high_score(self.difficulty), self.game_data.coins)
        self.settings_menu = SettingsMenu(self.screen, self.difficulty)
        self.game_over_screen = GameOverScreen(self.screen)
        self.pause_screen = PauseScreen(self.screen)
        self.shop_menu = ShopMenu(self.screen, self.game_data)
        self.minigame_menu = MiniGameMenu(self.screen)
        
    def init_minigames(self):
        """Initialize all mini-games"""
        self.time_attack = TimeAttackMode(self.screen, self.difficulty)
        self.zen_mode = ZenMode(self.screen)
        self.daily_challenge = DailyChallenge(self.screen)
        
        # New mini-games
        self.bird_battle = BirdBattle(self.screen, self.difficulty)
        self.dodge_master = DodgeMaster(self.screen, self.difficulty)
        self.memory_flight = MemoryFlight(self.screen, self.difficulty)
        self.boss_rush = BossRush(self.screen, self.difficulty)
        self.treasure_hunt = TreasureHunt(self.screen, self.difficulty)
        
    def new_game(self):
        """Start new game based on mode"""
        # Clear sprites
        self.all_sprites.empty()
        self.pipes.empty()
        self.coins.empty()
        self.powerups.empty()
        self.particle_system.clear()
        
        # Reset
        self.score_manager.reset_current_score()
        self.coins_this_game = 0
        self.combo_count = 0
        self.score_multiplier = 1.0
        self.has_coin_magnet = False
        self.has_slow_motion = False
        self.has_score_boost = False
        
        skin = self.game_data.current_skin
        
        # Start appropriate mode
        if self.game_mode == "bird_battle":
            self.bird_battle.start(skin)
            self.state = "minigame_battle"
            return
        elif self.game_mode == "dodge_master":
            self.dodge_master.start(skin)
            self.state = "minigame_dodge"
            return
        elif self.game_mode == "memory_flight":
            self.memory_flight.start(skin)
            self.state = "minigame_memory"
            return
        elif self.game_mode == "boss_rush":
            self.boss_rush.start(skin)
            self.state = "minigame_boss"
            return
        elif self.game_mode == "treasure_hunt":
            self.treasure_hunt.start(skin)
            self.state = "minigame_treasure"
            return
        
        # Classic modes
        self.bird = Bird(self.difficulty, skin)
        self.all_sprites.add(self.bird)
        self.apply_skin_abilities(skin)
        
        self.last_pipe_spawn = pygame.time.get_ticks()
        self.last_coin_spawn = pygame.time.get_ticks()
        
        if self.game_mode == "time_attack":
            self.time_attack.start()
        elif self.game_mode == "zen":
            self.zen_mode.start()
        
        self.get_ready = True
        self.get_ready_timer = 1000
        self.state = STATE_PLAYING
        
    def apply_skin_abilities(self, skin_id):
        skin = SKINS.get(skin_id, {})
        ability = skin.get("ability")
        
        if ability == "shield":
            self.bird.activate_shield(3000)
        elif ability == "double_coins":
            self.score_multiplier = 2.0
        elif ability == "coin_magnet":
            self.has_coin_magnet = True
            self.magnet_timer = pygame.time.get_ticks() + 10000
        elif ability == "slow_time":
            self.has_slow_motion = True
            self.slow_timer = pygame.time.get_ticks() + 5000
        elif ability == "score_boost":
            self.has_score_boost = True
            self.score_boost_timer = pygame.time.get_ticks() + 15000
        
    def spawn_pipe(self):
        if self.game_mode == "zen":
            self.spawn_zen_coins()
            return
            
        now = pygame.time.get_ticks()
        diff = DIFFICULTIES[self.difficulty]
        freq = diff["pipe_frequency"]
        if self.has_slow_motion:
            freq = int(freq * 1.5)
        
        if now - self.last_pipe_spawn > freq:
            self.last_pipe_spawn = now
            pipe_gap = diff["pipe_gap"]
            min_y = GROUND_HEIGHT + pipe_gap // 2 + 60
            max_y = SCREEN_HEIGHT - GROUND_HEIGHT - pipe_gap // 2 - 60
            gap_y = random.randint(min_y, max_y)
            
            top = Pipe((SCREEN_WIDTH, gap_y - pipe_gap // 2), True, self.difficulty)
            bottom = Pipe((SCREEN_WIDTH, gap_y + pipe_gap // 2), False, self.difficulty)
            self.pipes.add(top, bottom)
            self.all_sprites.add(top, bottom)
            
            if random.random() < 0.6:
                self.coins.add(Coin(SCREEN_WIDTH + 30, gap_y, self.difficulty))
            if random.random() < 0.05:
                self.powerups.add(PowerUp(SCREEN_WIDTH + 60, gap_y, random.choice(list(POWERUPS.keys())), self.difficulty))
                
    def spawn_zen_coins(self):
        now = pygame.time.get_ticks()
        if now - self.last_coin_spawn > 800:
            self.last_coin_spawn = now
            y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100)
            self.coins.add(Coin(SCREEN_WIDTH + 20, y, self.difficulty))
            
    def check_collisions(self):
        if not self.bird or not self.bird.alive:
            return
        
        for coin in list(self.coins):
            if self.bird.rect.colliderect(coin.rect):
                coin.kill()
                self.coins_this_game += int(COIN_VALUE * self.score_multiplier)
                self.particle_system.emit_score(coin.rect.centerx, coin.rect.centery)
                if self.game_mode == "zen":
                    self.zen_mode.add_coin()
                
        for powerup in list(self.powerups):
            if self.bird.rect.colliderect(powerup.rect):
                self.activate_powerup(powerup.power_type)
                powerup.kill()
        
        if self.has_coin_magnet:
            for coin in self.coins:
                dx = coin.rect.centerx - self.bird.rect.centerx
                dy = coin.rect.centery - self.bird.rect.centery
                if dx*dx + dy*dy < 22500:
                    coin.attract_to(self.bird)
        
        if self.game_mode == "zen":
            if self.bird.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
                self.bird.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                self.game_over()
            if self.bird.rect.top <= 0:
                self.bird.rect.top = 0
            return
            
        if not self.bird.is_protected():
            for pipe in self.pipes:
                if self.bird.rect.colliderect(pipe.rect):
                    if self.bird.get_mask().overlap(pipe.get_mask(), (pipe.rect.x - self.bird.rect.x, pipe.rect.y - self.bird.rect.y)):
                        self.game_over()
                        return
        
        if self.bird.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.bird.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.game_over()
        elif self.bird.rect.top <= 0:
            self.bird.rect.top = 0
            if not self.bird.is_protected():
                self.game_over()
                
    def activate_powerup(self, ptype):
        now = pygame.time.get_ticks()
        dur = POWERUPS.get(ptype, {}).get("duration", 5000)
        if ptype == "shield":
            self.bird.activate_shield(dur)
        elif ptype == "coin_magnet":
            self.has_coin_magnet = True
            self.magnet_timer = now + dur
        elif ptype == "slow_time":
            self.has_slow_motion = True
            self.slow_timer = now + dur
        elif ptype == "score_boost":
            self.has_score_boost = True
            self.score_boost_timer = now + dur
            self.score_multiplier = 2.0
            
    def update_powerups(self):
        now = pygame.time.get_ticks()
        if self.has_coin_magnet and now > self.magnet_timer:
            self.has_coin_magnet = False
        if self.has_slow_motion and now > self.slow_timer:
            self.has_slow_motion = False
        if self.has_score_boost and now > self.score_boost_timer:
            self.has_score_boost = False
            self.score_multiplier = 1.0
            
    def check_score(self):
        if not self.bird or self.game_mode == "zen":
            return
        for pipe in self.pipes:
            if not pipe.is_top and pipe.rect.right < self.bird.rect.left and not pipe.scored:
                pipe.scored = True
                for o in self.pipes:
                    if o.is_top and abs(o.rect.x - pipe.rect.x) < 10:
                        o.scored = True
                pts = 2 if self.has_score_boost else 1
                self.combo_count += 1
                if self.combo_count >= COMBO_THRESHOLD:
                    pts = int(pts * COMBO_MULTIPLIER)
                self.score_manager.increment_score(pts)
                self.particle_system.emit_score(self.bird.rect.centerx, self.bird.rect.top - 20)
                if self.game_mode == "time_attack":
                    self.time_attack.add_score(pts)
                    
    def game_over(self):
        self.bird.die()
        self.particle_system.emit_death(self.bird.rect.centerx, self.bird.rect.centery)
        self.game_data.add_coins(self.coins_this_game)
        self.game_data.record_game(self.score_manager.current_score)
        is_new = self.score_manager.update_score(self.score_manager.current_score, self.difficulty)
        if is_new:
            self.particle_system.emit_new_highscore(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        medal = self.score_manager.get_medal()
        self.game_over_screen.set_scores(self.score_manager.current_score, self.score_manager.get_high_score(self.difficulty), is_new, medal, self.coins_this_game)
        self.state = STATE_GAME_OVER
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if self.state == STATE_MENU:
                action = self.main_menu.handle_event(event)
                if action == "play":
                    self.state = "modes"
                elif action == "shop":
                    self.state = STATE_SHOP
                elif action == "settings":
                    self.state = STATE_SETTINGS
                    
            elif self.state == "modes":
                action = self.minigame_menu.handle_event(event)
                if action:
                    if action[0] == "back":
                        self.state = STATE_MENU
                    elif action[0] == "select_mode":
                        self.game_mode = action[1]
                        self.new_game()
                    
            elif self.state == STATE_SETTINGS:
                action = self.settings_menu.handle_event(event)
                if action:
                    if action[0] == "difficulty":
                        self.difficulty = action[1]
                        self.main_menu.high_score = self.score_manager.get_high_score(self.difficulty)
                    elif action[0] == "back":
                        self.state = STATE_MENU
                        
            elif self.state == STATE_SHOP:
                action = self.shop_menu.handle_event(event)
                if action and action[0] == "back":
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                        
            elif self.state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.bird and self.bird.alive:
                        self.bird.jump()
                    elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.state = STATE_PAUSED
                elif event.type == pygame.MOUSEBUTTONDOWN and self.bird and self.bird.alive:
                    self.bird.jump()
                    
            elif self.state == STATE_PAUSED:
                action = self.pause_screen.handle_event(event)
                if action == "resume":
                    self.state = STATE_PLAYING
                elif action == "restart":
                    self.new_game()
                elif action == "menu":
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    
            elif self.state == STATE_GAME_OVER:
                action = self.game_over_screen.handle_event(event)
                if action == "retry":
                    self.new_game()
                elif action == "menu":
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    self.main_menu.high_score = self.score_manager.get_high_score(self.difficulty)
                    
            # Mini-game states
            elif self.state == "minigame_battle":
                action = self.bird_battle.handle_event(event)
                if action == "done":
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    
            elif self.state == "minigame_dodge":
                action = self.dodge_master.handle_event(event)
                if action == "done":
                    self.game_data.add_coins(self.dodge_master.score // 10)
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    
            elif self.state == "minigame_memory":
                action = self.memory_flight.handle_event(event)
                if action == "done":
                    self.game_data.add_coins(self.memory_flight.score * 5)
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    
            elif self.state == "minigame_boss":
                action = self.boss_rush.handle_event(event)
                if action == "done":
                    if self.boss_rush.victory:
                        hits = self.boss_rush.hits_taken
                        reward = 200 if hits == 0 else (100 if hits <= 2 else (50 if hits <= 4 else 25))
                        self.game_data.add_coins(reward)
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    
            elif self.state == "minigame_treasure":
                action = self.treasure_hunt.handle_event(event)
                if action == "done":
                    if self.treasure_hunt.victory:
                        self.game_data.add_coins(50)
                    self.state = STATE_MENU
                    self.main_menu.coins = self.game_data.coins
                    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == STATE_MENU:
            self.main_menu.update(mouse_pos)
            self.background.update()
            self.ground.update()
        elif self.state == "modes":
            self.minigame_menu.update(mouse_pos)
        elif self.state == STATE_SETTINGS:
            self.settings_menu.update(mouse_pos)
        elif self.state == STATE_SHOP:
            self.shop_menu.update(mouse_pos)
        elif self.state == STATE_PLAYING:
            if self.get_ready:
                self.get_ready_timer -= self.dt
                if self.get_ready_timer <= 0:
                    self.get_ready = False
                return
            self.all_sprites.update()
            self.coins.update()
            self.powerups.update()
            self.background.update()
            self.ground.update()
            self.update_powerups()
            self.spawn_pipe()
            self.check_collisions()
            self.check_score()
            self.particle_system.update(self.dt)
            self.score_display.set_score(self.score_manager.current_score)
            if self.game_mode == "time_attack" and self.time_attack.update():
                self.game_over()
            elif self.game_mode == "zen":
                self.zen_mode.update(self.dt)
        elif self.state == STATE_PAUSED:
            self.pause_screen.update(mouse_pos)
        elif self.state == STATE_GAME_OVER:
            self.game_over_screen.update(mouse_pos)
            self.particle_system.update(self.dt)
        # Mini-games
        elif self.state == "minigame_battle":
            self.bird_battle.update(self.dt)
        elif self.state == "minigame_dodge":
            self.dodge_master.update(self.dt)
        elif self.state == "minigame_memory":
            self.memory_flight.update(self.dt)
        elif self.state == "minigame_boss":
            self.boss_rush.update(self.dt)
        elif self.state == "minigame_treasure":
            self.treasure_hunt.update(self.dt)
            
    def draw(self):
        if self.state == STATE_MENU:
            self.main_menu.draw(self.background, self.ground)
        elif self.state == "modes":
            self.minigame_menu.draw(self.background, self.ground)
        elif self.state == STATE_SETTINGS:
            self.settings_menu.draw(self.background, self.ground)
        elif self.state == STATE_SHOP:
            self.shop_menu.draw(self.background, self.ground)
        elif self.state == STATE_PLAYING:
            self.background.draw(self.screen)
            for p in self.pipes:
                self.screen.blit(p.image, p.rect)
            for c in self.coins:
                self.screen.blit(c.image, c.rect)
            for p in self.powerups:
                self.screen.blit(p.image, p.rect)
            self.ground.draw(self.screen)
            if self.bird:
                self.bird.draw_effects(self.screen)
                self.screen.blit(self.bird.image, self.bird.rect)
            self.particle_system.draw(self.screen)
            self.draw_hud()
            if self.get_ready:
                self.draw_get_ready()
        elif self.state == STATE_PAUSED:
            self.draw_game_state()
            self.pause_screen.draw()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_state()
            self.particle_system.draw(self.screen)
            self.game_over_screen.draw()
        # Mini-games
        elif self.state == "minigame_battle":
            self.bird_battle.draw(self.background, self.ground)
        elif self.state == "minigame_dodge":
            self.dodge_master.draw(self.background, self.ground)
        elif self.state == "minigame_memory":
            self.memory_flight.draw(self.background, self.ground)
        elif self.state == "minigame_boss":
            self.boss_rush.draw(self.background, self.ground)
        elif self.state == "minigame_treasure":
            self.treasure_hunt.draw(self.background, self.ground)
            
        pygame.display.flip()
        
    def draw_game_state(self):
        self.background.draw(self.screen)
        for p in self.pipes:
            self.screen.blit(p.image, p.rect)
        self.ground.draw(self.screen)
        if self.bird:
            self.screen.blit(self.bird.image, self.bird.rect)
        
    def draw_hud(self):
        if self.game_mode != "zen":
            self.score_display.draw(self.screen)
        coin_text = f"{self.coins_this_game}"
        coin_surf = self.hud_font.render(coin_text, True, COIN_COLOR)
        self.screen.blit(coin_surf, (SCREEN_WIDTH - 50, 15))
        pygame.draw.circle(self.screen, COIN_COLOR, (SCREEN_WIDTH - 65, 23), 8)
        if self.game_mode == "time_attack":
            self.time_attack.draw_timer()
        elif self.game_mode == "zen":
            self.zen_mode.draw_hud()
        if self.combo_count >= COMBO_THRESHOLD:
            combo = self.hud_font.render(f"COMBO x{self.combo_count}!", True, PRIMARY_COLOR)
            self.screen.blit(combo, (SCREEN_WIDTH // 2 - combo.get_width() // 2, 85))
            
    def draw_get_ready(self):
        font = pygame.font.Font(None, 48)
        shadow = font.render("Get Ready!", True, TEXT_SHADOW)
        self.screen.blit(shadow, (SCREEN_WIDTH // 2 - shadow.get_width() // 2 + 2, SCREEN_HEIGHT // 2 + 2))
        text = font.render("Get Ready!", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        small = pygame.font.Font(None, 26)
        tap = small.render("Tap or SPACE to fly!", True, (200, 200, 200))
        self.screen.blit(tap, (SCREEN_WIDTH // 2 - tap.get_width() // 2, SCREEN_HEIGHT // 2 + 45))
        
    async def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)  # Allow browser to handle events
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
