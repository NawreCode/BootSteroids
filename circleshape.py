import pygame


class CircleShape(pygame.sprite.Sprite):
    """Base class for game objects"""

    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def isColliding(self, shape):
        d = self.position.distance_to(shape.position)
        if d > self.radius + shape.radius:
            return False
        return True
