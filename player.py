import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_ACCELERATION, PLAYER_DRAG
from shot import Shot


class Player(CircleShape):
    """Player class representing the player in the game."""

    shoot_cooldown = 0 # Cooldown for shooting

    def __init__(self, x: int, y: int, sound_manager=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.sound_manager = sound_manager
        self.velocity = pygame.Vector2(0, 0)  # Add velocity for momentum

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(
            self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def thrust(self, dt, direction=1):
        """Apply thrust in the forward direction (direction=1) or backward (direction=-1)"""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        acceleration = forward * PLAYER_ACCELERATION * direction * dt
        self.velocity += acceleration

    def wrap_screen(self):
        """Wrap player position around screen edges"""
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def update(self, dt):
        self.shoot_cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_z]:
            self.thrust(dt, 1)  # Forward thrust
        if keys[pygame.K_s]:
            self.thrust(dt, -1)  # Backward thrust
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Apply frame-rate independent drag to velocity
        # Convert per-frame drag to per-second drag for consistency
        drag_per_second = PLAYER_DRAG ** (dt * 60)  # Assuming 60 FPS as baseline
        self.velocity *= drag_per_second
        
        # Update position based on velocity
        self.position += self.velocity * dt
        
        self.wrap_screen()

    def shoot(self):
        # Prevent rapid-fire abuse by enforcing cooldown timer
        if self.shoot_cooldown > 0:
            return
        
        # Play shooting sound
        if self.sound_manager:
            self.sound_manager.play_sound('shoot')
        
        shot = Shot(self.position[0], self.position[1])
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        
        # Reset cooldown to prevent rapid-fire abuse
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
