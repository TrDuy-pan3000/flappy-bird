import pygame
import random
import math
from settings import *

class Particle:
    def __init__(self, x, y, color, velocity, lifetime=500, size=5, gravity=0.1):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = gravity
        self.alpha = 255
        
    def update(self, dt):
        """Update particle position and lifetime"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
        # Reduce lifetime
        self.lifetime -= dt
        
        # Fade out
        self.alpha = max(0, int(255 * (self.lifetime / self.max_lifetime)))
        
        return self.lifetime > 0
        
    def draw(self, screen):
        """Draw the particle"""
        if self.alpha <= 0:
            return
            
        # Create a surface with alpha
        size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        color_with_alpha = (*self.color[:3], self.alpha)
        pygame.draw.circle(surf, color_with_alpha, (size, size), size)
        
        screen.blit(surf, (int(self.x) - size, int(self.y) - size))


class ScoreParticle:
    """Floating +1 score indicator"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = -2
        self.lifetime = 600
        self.max_lifetime = 600
        self.alpha = 255
        self.font = pygame.font.Font(None, 36)
        
    def update(self, dt):
        self.y += self.vy
        self.vy *= 0.98  # Slow down
        self.lifetime -= dt
        self.alpha = max(0, int(255 * (self.lifetime / self.max_lifetime)))
        return self.lifetime > 0
        
    def draw(self, screen):
        if self.alpha <= 0:
            return
            
        text_surf = self.font.render("+1", True, PRIMARY_COLOR)
        text_surf.set_alpha(self.alpha)
        
        # Add shadow
        shadow_surf = self.font.render("+1", True, TEXT_SHADOW)
        shadow_surf.set_alpha(self.alpha)
        
        screen.blit(shadow_surf, (self.x + 2, self.y + 2))
        screen.blit(text_surf, (self.x, self.y))


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.score_particles = []
        
    def emit_death(self, x, y):
        """Emit particles when bird dies"""
        colors = [
            (255, 100, 100),  # Red
            (255, 150, 100),  # Orange
            (255, 200, 100),  # Yellow
            (255, 255, 255),  # White
        ]
        
        for _ in range(PARTICLE_COUNT):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2  # Bias upward
            
            color = random.choice(colors)
            size = random.randint(3, 8)
            lifetime = random.randint(300, 600)
            
            self.particles.append(Particle(x, y, color, (vx, vy), lifetime, size, 0.15))
            
    def emit_score(self, x, y):
        """Emit particles when scoring"""
        self.score_particles.append(ScoreParticle(x, y))
        
        # Also emit some sparkles
        colors = [PRIMARY_COLOR, (255, 255, 200), (255, 215, 0)]
        
        for _ in range(5):
            angle = random.uniform(-math.pi/2 - 0.5, -math.pi/2 + 0.5)  # Mostly upward
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice(colors)
            
            self.particles.append(Particle(x, y, color, (vx, vy), 400, 4, 0.05))
            
    def emit_new_highscore(self, x, y):
        """Special particles for new high score"""
        colors = [
            (255, 215, 0),    # Gold
            (255, 255, 100),  # Bright yellow
            (255, 200, 50),   # Orange gold
            (255, 255, 255),  # White sparkle
        ]
        
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice(colors)
            size = random.randint(4, 10)
            lifetime = random.randint(500, 1000)
            
            self.particles.append(Particle(x, y, color, (vx, vy), lifetime, size, 0.08))
            
    def update(self, dt):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update(dt)]
        self.score_particles = [p for p in self.score_particles if p.update(dt)]
        
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)
        for particle in self.score_particles:
            particle.draw(screen)
            
    def clear(self):
        """Clear all particles"""
        self.particles = []
        self.score_particles = []
