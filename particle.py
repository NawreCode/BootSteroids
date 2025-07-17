"""
Particle class for visual effects.
"""
import pygame
import math
import random


class Particle:
    """Individual particle for visual effects."""
    
    def __init__(self, position, velocity, color, lifetime, size=2):
        """
        Initialize a particle.
        
        Args:
            position: pygame.Vector2 - Starting position
            velocity: pygame.Vector2 - Initial velocity
            color: tuple - RGB color tuple
            lifetime: float - How long the particle lives in seconds
            size: int - Particle size in pixels
        """
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.initial_color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.initial_size = size
        
    def update(self, dt):
        """Update particle position and properties."""
        # Update position
        self.position += self.velocity * dt
        
        # Reduce lifetime
        self.lifetime -= dt
        
        # Fade out over time
        if self.max_lifetime > 0:
            life_ratio = self.lifetime / self.max_lifetime
            # Fade alpha and size
            alpha = max(0, int(255 * life_ratio))
            self.size = max(1, int(self.initial_size * life_ratio))
            
            # Create fading color
            r, g, b = self.initial_color
            self.color = (
                min(255, max(0, int(r * life_ratio))),
                min(255, max(0, int(g * life_ratio))),
                min(255, max(0, int(b * life_ratio)))
            )
    
    def draw(self, screen):
        """Draw the particle to the screen."""
        if self.lifetime > 0 and self.size > 0:
            pygame.draw.circle(screen, self.color, 
                             (int(self.position.x), int(self.position.y)), 
                             self.size)
    
    def is_alive(self):
        """Check if particle is still alive."""
        return self.lifetime > 0


class ParticleSystem:
    """Manages multiple particles for visual effects."""
    
    def __init__(self):
        """Initialize the particle system."""
        self.particles = []
    
    def emit_explosion(self, position, count=20, size="medium", color_scheme="orange"):
        """
        Create an explosion effect.
        
        Args:
            position: pygame.Vector2 - Center of explosion
            count: int - Number of particles to create
            size: str - "small", "medium", or "large" explosion
            color_scheme: str - "orange", "white", "blue", etc.
        """
        # Define size parameters
        size_params = {
            "small": {"speed_range": (50, 150), "lifetime_range": (0.5, 1.5), "particle_size": 2},
            "medium": {"speed_range": (75, 200), "lifetime_range": (0.8, 2.0), "particle_size": 3},
            "large": {"speed_range": (100, 250), "lifetime_range": (1.0, 2.5), "particle_size": 4}
        }
        
        # Define color schemes
        color_schemes = {
            "orange": [(255, 165, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0)],
            "white": [(255, 255, 255), (200, 200, 200), (150, 150, 150)],
            "blue": [(0, 100, 255), (0, 150, 255), (100, 200, 255)],
            "red": [(255, 0, 0), (255, 100, 100), (200, 0, 0)]
        }
        
        params = size_params.get(size, size_params["medium"])
        colors = color_schemes.get(color_scheme, color_schemes["orange"])
        
        for _ in range(count):
            # Random direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*params["speed_range"])
            
            # Create velocity vector
            velocity = pygame.Vector2(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            # Random color from scheme
            color = random.choice(colors)
            
            # Random lifetime
            lifetime = random.uniform(*params["lifetime_range"])
            
            # Create particle
            particle = Particle(position, velocity, color, lifetime, params["particle_size"])
            self.particles.append(particle)
    
    def emit_burst(self, position, velocity_direction, count=10, spread_angle=math.pi/3, 
                   color=(255, 255, 255), speed_range=(100, 200), lifetime_range=(0.5, 1.5)):
        """
        Create a directional burst of particles.
        
        Args:
            position: pygame.Vector2 - Starting position
            velocity_direction: pygame.Vector2 - Base direction for particles
            count: int - Number of particles
            spread_angle: float - Angle spread in radians
            color: tuple - RGB color
            speed_range: tuple - Min and max speed
            lifetime_range: tuple - Min and max lifetime
        """
        base_angle = math.atan2(velocity_direction.y, velocity_direction.x)
        
        for _ in range(count):
            # Random angle within spread
            angle_offset = random.uniform(-spread_angle/2, spread_angle/2)
            angle = base_angle + angle_offset
            speed = random.uniform(*speed_range)
            
            # Create velocity
            velocity = pygame.Vector2(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            # Random lifetime
            lifetime = random.uniform(*lifetime_range)
            
            # Create particle
            particle = Particle(position, velocity, color, lifetime)
            self.particles.append(particle)
    
    def emit_trail(self, position, velocity, count=5, color=(255, 255, 255), 
                   lifetime=0.5, size=1):
        """
        Create a trail effect behind a moving object.
        
        Args:
            position: pygame.Vector2 - Current position
            velocity: pygame.Vector2 - Current velocity
            count: int - Number of trail particles
            color: tuple - RGB color
            lifetime: float - How long trail particles last
            size: int - Particle size
        """
        for i in range(count):
            # Create particles behind the object
            offset_factor = (i + 1) * 0.1
            trail_pos = position - velocity * offset_factor
            
            # Create particle with reduced velocity
            particle_velocity = velocity * 0.1
            particle = Particle(trail_pos, particle_velocity, color, lifetime, size)
            self.particles.append(particle)
    
    def update(self, dt):
        """Update all particles."""
        # Update all particles
        for particle in self.particles[:]:  # Use slice to avoid modification during iteration
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(screen)