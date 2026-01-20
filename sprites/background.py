import pygame
import random
import math
from settings import *

class Background:
    """Optimized Tet-themed background with fireworks and lanterns"""
    
    _cached_surface = None
    _tet_cached = None
    
    def __init__(self, difficulty="medium"):
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"] * 0.3
        self.x = 0
        
        # Tet animations
        self.fireworks = []
        self.lanterns = []
        self.petals = []
        self.time = 0
        
        # Create cached background
        if TET_MODE:
            if Background._tet_cached is None:
                Background._tet_cached = self.create_tet_background()
            self.image = Background._tet_cached
            self.init_tet_effects()
        else:
            if Background._cached_surface is None:
                Background._cached_surface = self.create_background()
            self.image = Background._cached_surface
        
    def init_tet_effects(self):
        """Initialize Tet decorations"""
        # Lanterns
        for i in range(5):
            self.lanterns.append({
                'x': random.randint(30, SCREEN_WIDTH - 30),
                'y': random.randint(20, 100),
                'swing': random.uniform(0, math.pi * 2),
                'size': random.randint(20, 35),
                'color': random.choice([LANTERN_RED, LANTERN_GOLD])
            })
        
        # Initial petals
        for _ in range(15):
            self.petals.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(-0.5, -0.2),
                'vy': random.uniform(0.5, 1.5),
                'size': random.randint(3, 8),
                'rotation': random.uniform(0, 360),
                'color': random.choice([TET_PINK, TET_YELLOW, (255, 200, 200)])
            })
    
    def create_tet_background(self):
        """Create beautiful Tet night sky background"""
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Night sky gradient
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            ratio = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * ratio)
            g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * ratio)
            b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * ratio)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Stars
        random.seed(2026)  # Năm mới 2026
        for _ in range(80):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, int((SCREEN_HEIGHT - GROUND_HEIGHT) * 0.7))
            brightness = random.randint(150, 255)
            size = random.randint(1, 3)
            pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
        
        # Moon
        moon_x, moon_y = SCREEN_WIDTH - 70, 60
        pygame.draw.circle(surf, (255, 250, 220), (moon_x, moon_y), 35)
        pygame.draw.circle(surf, (240, 235, 200), (moon_x + 3, moon_y - 2), 30)  # Crater effect
        
        # Distant mountains/city silhouette for Tet
        city_y = SCREEN_HEIGHT - GROUND_HEIGHT - 80
        city_color = (30, 20, 40)
        
        # Traditional houses silhouette
        houses = [
            (0, 50, 35), (40, 65, 40), (85, 55, 35), (125, 75, 45),
            (175, 60, 35), (215, 70, 40), (260, 55, 35), (300, 80, 45), (350, 60, 35)
        ]
        
        for x, h, w in houses:
            # House body
            pygame.draw.rect(surf, city_color, (x, city_y - h + 50, w, h))
            # Traditional roof
            pygame.draw.polygon(surf, (40, 25, 50), [
                (x - 5, city_y - h + 50),
                (x + w // 2, city_y - h + 30),
                (x + w + 5, city_y - h + 50)
            ])
            # Windows with warm light
            for wy in range(city_y - h + 58, city_y + 40, 12):
                for wx in range(x + 5, x + w - 5, 10):
                    if random.random() > 0.3:
                        pygame.draw.rect(surf, (255, 200, 100, 150), (wx, wy, 5, 6))
        
        return surf
        
    def create_background(self):
        """Create default sky background"""
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            ratio = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(135 + (176 - 135) * ratio)
            g = int(206 + (224 - 206) * ratio)
            b = int(250 + (230 - 250) * ratio)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        cloud_data = [(40, 50), (150, 80), (280, 40), (60, 150), (220, 170), (350, 100)]
        for cx, cy in cloud_data:
            pygame.draw.circle(surf, (255, 255, 255), (cx, cy), 25)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 20, cy - 5), 20)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 35, cy), 22)
            pygame.draw.circle(surf, (255, 255, 255), (cx - 15, cy + 5), 18)
            pygame.draw.circle(surf, (255, 255, 255), (cx + 15, cy + 8), 20)
        
        city_y = SCREEN_HEIGHT - GROUND_HEIGHT - 60
        city_color = (120, 130, 160)
        
        buildings = [
            (0, 40), (25, 55), (50, 35), (75, 70), (100, 50),
            (125, 60), (150, 45), (175, 80), (200, 55), (225, 65),
            (250, 50), (275, 40), (300, 75), (325, 55), (350, 60), (375, 45)
        ]
        
        for x, h in buildings:
            pygame.draw.rect(surf, city_color, (x, city_y - h + 40, 22, h))
            for wy in range(city_y - h + 45, city_y + 35, 8):
                for wx in range(x + 3, x + 19, 6):
                    pygame.draw.rect(surf, (180, 180, 150), (wx, wy, 3, 4))
        
        return surf
    
    def spawn_firework(self):
        """Spawn a new firework"""
        if len(self.fireworks) < 3:
            self.fireworks.append(Firework(
                random.randint(50, SCREEN_WIDTH - 50),
                SCREEN_HEIGHT - GROUND_HEIGHT
            ))
    
    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -SCREEN_WIDTH:
            self.x = 0
        
        self.time += 1
        
        if TET_MODE:
            # Update lanterns swing
            for lantern in self.lanterns:
                lantern['swing'] += 0.03
            
            # Update petals
            for petal in self.petals:
                petal['x'] += petal['vx']
                petal['y'] += petal['vy']
                petal['rotation'] += 2
                
                # Wrap around
                if petal['y'] > SCREEN_HEIGHT - GROUND_HEIGHT:
                    petal['y'] = -10
                    petal['x'] = random.randint(0, SCREEN_WIDTH)
                if petal['x'] < -10:
                    petal['x'] = SCREEN_WIDTH + 10
            
            # Update fireworks
            for fw in self.fireworks[:]:
                fw.update()
                if fw.done:
                    self.fireworks.remove(fw)
            
            # Spawn new fireworks occasionally
            if random.random() < 0.01:
                self.spawn_firework()
            
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), 0))
        screen.blit(self.image, (int(self.x) + SCREEN_WIDTH, 0))
        
        if TET_MODE:
            # Draw petals
            for petal in self.petals:
                self.draw_petal(screen, petal)
            
            # Draw lanterns
            for lantern in self.lanterns:
                self.draw_lantern(screen, lantern)
            
            # Draw fireworks
            for fw in self.fireworks:
                fw.draw(screen)
    
    def draw_petal(self, screen, petal):
        """Draw a falling petal"""
        x, y = int(petal['x']), int(petal['y'])
        size = petal['size']
        
        # Simple petal shape
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, petal['color'], (0, size // 2, size * 2, size))
        
        # Rotate
        rotated = pygame.transform.rotate(surf, petal['rotation'])
        rect = rotated.get_rect(center=(x, y))
        screen.blit(rotated, rect)
    
    def draw_lantern(self, screen, lantern):
        """Draw a swinging lantern"""
        x = lantern['x'] + math.sin(lantern['swing']) * 8
        y = lantern['y']
        size = lantern['size']
        color = lantern['color']
        
        # String
        pygame.draw.line(screen, (100, 80, 60), (int(x), 0), (int(x), int(y) - size // 2), 2)
        
        # Lantern body (oval)
        pygame.draw.ellipse(screen, color, (int(x) - size // 2, int(y) - size // 2, size, int(size * 1.3)))
        
        # Inner glow
        glow_color = (min(255, color[0] + 50), min(255, color[1] + 50), color[2])
        pygame.draw.ellipse(screen, glow_color, (int(x) - size // 3, int(y) - size // 3, size * 2 // 3, size))
        
        # Top handle
        pygame.draw.rect(screen, (80, 60, 40), (int(x) - size // 4, int(y) - size // 2 - 5, size // 2, 8))
        
        # Bottom tip
        pygame.draw.polygon(screen, color, [
            (int(x) - size // 4, int(y) + int(size * 0.8) - size // 2),
            (int(x), int(y) + int(size * 1.1) - size // 2),
            (int(x) + size // 4, int(y) + int(size * 0.8) - size // 2)
        ])


class Firework:
    """Firework particle effect"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_y = random.randint(80, 200)
        self.vy = -random.uniform(8, 12)
        self.phase = "rising"  # rising, exploding, fading
        self.particles = []
        self.done = False
        self.color = random.choice(FIREWORK_COLORS)
        
    def update(self):
        if self.phase == "rising":
            self.y += self.vy
            self.vy += 0.15  # Gravity
            
            if self.y <= self.target_y or self.vy >= 0:
                self.phase = "exploding"
                self.explode()
                
        elif self.phase == "exploding" or self.phase == "fading":
            self.phase = "fading"
            all_done = True
            
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.08  # Gravity
                p['life'] -= 0.02
                
                if p['life'] > 0:
                    all_done = False
            
            if all_done:
                self.done = True
    
    def explode(self):
        """Create explosion particles"""
        num_particles = random.randint(30, 50)
        
        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': self.color,
                'size': random.randint(2, 4)
            })
    
    def draw(self, screen):
        if self.phase == "rising":
            # Draw trail
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 2)
            
        else:
            for p in self.particles:
                if p['life'] > 0:
                    alpha = int(255 * p['life'])
                    size = int(p['size'] * p['life'])
                    if size > 0:
                        color = (
                            min(255, int(p['color'][0])),
                            min(255, int(p['color'][1])),
                            min(255, int(p['color'][2]))
                        )
                        pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), size)


class Ground(pygame.sprite.Sprite):
    """Optimized Tet-themed ground"""
    
    _cached_surface = None
    _tet_cached = None
    
    def __init__(self, difficulty="medium"):
        super().__init__()
        
        diff_settings = DIFFICULTIES.get(difficulty, DIFFICULTIES["medium"])
        self.scroll_speed = diff_settings["scroll_speed"]
        self.x = 0
        
        if TET_MODE:
            if Ground._tet_cached is None:
                Ground._tet_cached = self.create_tet_ground()
            self.image = Ground._tet_cached
        else:
            if Ground._cached_surface is None:
                Ground._cached_surface = self.create_ground()
            self.image = Ground._cached_surface
            
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    
    def create_tet_ground(self):
        """Create festive Tet ground"""
        surf = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Red festive path
        pygame.draw.rect(surf, (139, 69, 19), (0, 0, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Gold trim at top
        pygame.draw.rect(surf, TET_GOLD, (0, 0, SCREEN_WIDTH, 8))
        pygame.draw.rect(surf, (200, 160, 0), (0, 8, SCREEN_WIDTH, 4))
        
        # Decorative pattern
        random.seed(88)  # Lucky number
        for x in range(0, SCREEN_WIDTH, 40):
            # Red patterns
            pygame.draw.circle(surf, TET_RED, (x + 20, 25), 8)
            pygame.draw.circle(surf, TET_GOLD, (x + 20, 25), 4)
        
        # Soil texture
        for _ in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(35, GROUND_HEIGHT - 5)
            pygame.draw.circle(surf, (120, 60, 20), (x, y), 2)
        
        return surf
        
    def create_ground(self):
        """Create ground surface"""
        surf = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        
        pygame.draw.rect(surf, (100, 180, 80), (0, 0, SCREEN_WIDTH, 18))
        
        for x in range(0, SCREEN_WIDTH, 5):
            pygame.draw.line(surf, (80, 160, 60), (x, 18), (x + 2, 0), 2)
        
        pygame.draw.rect(surf, (139, 90, 43), (0, 18, SCREEN_WIDTH, GROUND_HEIGHT - 18))
        
        random.seed(42)
        for _ in range(40):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(22, GROUND_HEIGHT - 5)
            pygame.draw.circle(surf, (160, 110, 60), (x, y), 2)
            
        return surf
                
    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -SCREEN_WIDTH:
            self.x = 0
            
    def draw(self, screen):
        y = SCREEN_HEIGHT - GROUND_HEIGHT
        screen.blit(self.image, (int(self.x), y))
        screen.blit(self.image, (int(self.x) + SCREEN_WIDTH, y))
