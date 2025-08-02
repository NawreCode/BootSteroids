import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS, SCREEN_WIDTH, SCREEN_HEIGHT


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rotation_speed = random.uniform(-180, 180)  # degrees per second

    def draw(self, screen):
        # Draw asteroid as an irregular polygon that rotates
        import math
        
        # Create points for an irregular asteroid shape
        num_points = 8
        points = []
        
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi + math.radians(self.rotation)
            # Add some randomness to make it look more like an asteroid
            radius_variation = random.uniform(0.7, 1.3) if hasattr(self, '_shape_seed') else 1.0
            if not hasattr(self, '_shape_seed'):
                # Create a consistent shape seed for this asteroid
                self._shape_seed = random.randint(0, 1000)
                random.seed(self._shape_seed)
                self._radius_variations = [random.uniform(0.7, 1.3) for _ in range(num_points)]
                random.seed()  # Reset to random seed
            
            actual_radius = self.radius * self._radius_variations[i]
            x = self.position.x + math.cos(angle) * actual_radius
            y = self.position.y + math.sin(angle) * actual_radius
            points.append((x, y))
        
        # Draw the asteroid polygon
        if len(points) > 2:
            pygame.draw.polygon(screen, "white", points, 2)

    def wrap_screen(self):
        """Wrap asteroid position around screen edges"""
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rotation += self.rotation_speed * dt
        self.wrap_screen()

    def split(self):
        # Calculate points based on asteroid size before destroying
        max_radius = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
        
        if self.radius >= max_radius:
            points = 20  # Large asteroid
        elif self.radius >= ASTEROID_MIN_RADIUS * 2:
            points = 50  # Medium asteroid
        else:
            points = 100  # Small asteroid
        
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return points

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Improved velocity distribution for more realistic splitting
        # Use a wider angle range and add some randomness to speed
        base_angle = random.uniform(30, 60)  # Wider angle range
        speed_multiplier = random.uniform(1.1, 1.5)  # More varied speed
        
        # Add some perpendicular velocity component for more interesting trajectories
        perpendicular_velocity = pygame.Vector2(-self.velocity.y, self.velocity.x).normalize() * random.uniform(-30, 30)
        
        velocity1 = self.velocity.rotate(base_angle) * speed_multiplier + perpendicular_velocity
        velocity2 = self.velocity.rotate(-base_angle) * speed_multiplier - perpendicular_velocity

        # Create new asteroids with proper sprite group membership
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.position = self.position.copy()
        asteroid1.velocity = velocity1
        # Inherit rotation characteristics with some variation
        asteroid1.rotation = self.rotation + random.uniform(-45, 45)
        asteroid1.rotation_speed = self.rotation_speed + random.uniform(-60, 60)

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.position = self.position.copy()
        asteroid2.velocity = velocity2
        # Inherit rotation characteristics with some variation
        asteroid2.rotation = self.rotation + random.uniform(-45, 45)
        asteroid2.rotation_speed = self.rotation_speed + random.uniform(-60, 60)
        
        return points
