import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

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
        random_angle = random.uniform(20, 50)

        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.position = self.position.copy()
        asteroid1.velocity = velocity1 * 1.2

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.position = self.position.copy()
        asteroid2.velocity = velocity2 * 1.2
        
        return points
