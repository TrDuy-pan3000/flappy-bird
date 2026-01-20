import pygame
import random
from settings import *
from sprites.bird import Bird
from sprites.projectile import ColorGate

class MemoryFlight:
    """Memory Flight puzzle mini-game - Simon Says style"""
    
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty
        
        # Game state
        self.is_active = False
        self.is_over = False
        self.score = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Sprites
        self.player = None
        self.gates = []
        
        # Sequence
        self.sequence = []
        self.player_sequence = []
        self.current_highlight = 0
        
        # States: showing, playing, feedback
        self.state = "showing"
        self.state_timer = 0
        
        # Colors
        self.colors = ["red", "blue", "yellow", "purple", "orange"]
        
        # Timing
        self.show_time = 800  # ms per color shown
        self.answer_time = 5000  # ms to answer each
        self.last_answer = 0
        
    def start(self, skin_id="default"):
        """Start new game"""
        self.is_active = True
        self.is_over = False
        self.score = 0
        
        # Create player
        self.player = Bird(self.difficulty, skin_id)
        self.player.rect.left = 30
        self.player.rect.centery = SCREEN_HEIGHT // 2
        self.player.gravity = 0.15
        
        # Create gates
        self.gates = []
        gate_spacing = (SCREEN_WIDTH - 100) // len(self.colors)
        for i, color in enumerate(self.colors):
            x = 80 + i * gate_spacing
            gate = ColorGate(x, color)
            self.gates.append(gate)
            
        # Start first sequence
        self.sequence = []
        self.player_sequence = []
        self.add_to_sequence()
        self.start_showing()
        
    def add_to_sequence(self):
        """Add random color to sequence"""
        self.sequence.append(random.choice(self.colors))
        
    def start_showing(self):
        """Start showing sequence"""
        self.state = "showing"
        self.current_highlight = 0
        self.state_timer = pygame.time.get_ticks()
        
        # Reset gates
        for gate in self.gates:
            gate.reset()
            
    def start_playing(self):
        """Player turn to repeat"""
        self.state = "playing"
        self.player_sequence = []
        self.last_answer = pygame.time.get_ticks()
        
        # Reset player position
        self.player.rect.left = 30
        self.player.rect.centery = SCREEN_HEIGHT // 2
        self.player.velocity = 0
        
    def update(self, dt):
        if not self.is_active or self.is_over:
            return
            
        now = pygame.time.get_ticks()
        
        # Update player
        if self.player and self.player.alive and self.state == "playing":
            # Apply gravity
            self.player.velocity += self.player.gravity
            self.player.rect.y += int(self.player.velocity)
            
            # Bounds
            if self.player.rect.top < 0:
                self.player.rect.top = 0
                self.player.velocity = 0
            if self.player.rect.bottom > SCREEN_HEIGHT - GROUND_HEIGHT:
                self.player.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
                self.player.velocity = 0
                
            # Move forward
            self.player.rect.x += 2
            
            # Check gate collision
            self.check_gate_collision()
            
            # Check timeout
            if now - self.last_answer > self.answer_time:
                self.game_over("timeout")
                
        # Showing state
        elif self.state == "showing":
            elapsed = now - self.state_timer
            
            # Calculate which color to highlight
            color_index = elapsed // self.show_time
            
            if color_index >= len(self.sequence):
                # Done showing, player turn
                for gate in self.gates:
                    gate.highlight(False)
                self.start_playing()
            else:
                # Highlight current color
                current_color = self.sequence[color_index]
                for gate in self.gates:
                    gate.highlight(gate.color_name == current_color)
                    
        elif self.state == "feedback":
            # Brief pause after each answer
            if now - self.state_timer > 500:
                if len(self.player_sequence) >= len(self.sequence):
                    # Completed sequence!
                    self.score += 1
                    self.add_to_sequence()
                    self.start_showing()
                else:
                    # Continue playing
                    self.state = "playing"
                    self.last_answer = now
                    
    def check_gate_collision(self):
        """Check if player passed through a gate"""
        for gate in self.gates:
            if self.player.rect.colliderect(gate.rect):
                # Only register once per gate pass
                if gate.color_name not in [g for g in self.player_sequence[-1:] if self.player_sequence]:
                    self.register_answer(gate.color_name)
                    return
                    
    def register_answer(self, color):
        """Register player's answer"""
        now = pygame.time.get_ticks()
        expected_index = len(self.player_sequence)
        
        if expected_index >= len(self.sequence):
            return
            
        expected_color = self.sequence[expected_index]
        
        # Find the gate
        for gate in self.gates:
            if gate.color_name == color:
                if color == expected_color:
                    # Correct!
                    gate.set_feedback(True)
                    self.player_sequence.append(color)
                    self.state = "feedback"
                    self.state_timer = now
                else:
                    # Wrong!
                    gate.set_feedback(False)
                    self.game_over("wrong")
                break
                
        self.last_answer = now
        
    def game_over(self, reason):
        """Handle game over"""
        self.is_over = True
        if self.player:
            self.player.alive = False
            
    def draw(self, background, ground):
        """Draw game"""
        background.draw(self.screen)
        
        # Gates
        for gate in self.gates:
            self.screen.blit(gate.image, gate.rect)
            
        ground.draw(self.screen)
        
        # Player
        if self.player and self.state == "playing":
            self.screen.blit(self.player.image, self.player.rect)
            
        # HUD
        self.draw_hud()
        
        if self.is_over:
            self.draw_game_over()
            
    def draw_hud(self):
        """Draw HUD"""
        # Score (sequence length)
        score = self.font.render(f"Level: {self.score + 1}", True, WHITE)
        self.screen.blit(score, (20, 20))
        
        # Sequence length
        seq = self.font.render(f"Sequence: {len(self.sequence)}", True, PRIMARY_COLOR)
        self.screen.blit(seq, (SCREEN_WIDTH - 180, 20))
        
        # State indicator
        if self.state == "showing":
            text = "WATCH THE SEQUENCE..."
            color = (255, 200, 100)
        elif self.state == "playing":
            text = f"YOUR TURN! ({len(self.player_sequence)}/{len(self.sequence)})"
            color = (100, 255, 100)
        else:
            text = ""
            color = WHITE
            
        if text:
            state = self.font.render(text, True, color)
            self.screen.blit(state, (SCREEN_WIDTH // 2 - state.get_width() // 2, 60))
            
    def draw_game_over(self):
        """Draw game over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        title = self.big_font.render("GAME OVER", True, ACCENT_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 180))
        
        score = self.font.render(f"You remembered {self.score} sequences!", True, WHITE)
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, 280))
        
        hint = self.font.render("Press SPACE to continue", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 360))
        
    def handle_event(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.is_over:
                    return "done"
                elif self.state == "playing" and self.player:
                    self.player.velocity = -5
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over:
                return "done"
            elif self.state == "playing" and self.player:
                self.player.velocity = -5
                
        return None
