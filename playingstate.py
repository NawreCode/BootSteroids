"""
PlayingState class for active gameplay.
"""
import pygame
from gamestate import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


class PlayingState(GameState):
    """Active gameplay state."""
    
    def __init__(self, state_manager):
        """Initialize the playing state."""
        super().__init__(state_manager)
        self.updatable = None
        self.drawable = None
        self.asteroids = None
        self.shots = None
        self.player = None
        self.asteroid_field = None
    
    def enter(self):
        """Called when entering the playing state."""
        print("Entered Playing State")
        
        # Initialize sprite groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Set up containers for game objects
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable,)
        Player.containers = (self.updatable, self.drawable)
        Shot.containers = (self.updatable, self.drawable, self.shots)
        
        # Create player and asteroid field
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2
        self.player = Player(x, y)
        self.asteroid_field = AsteroidField()
    
    def exit(self):
        """Called when leaving the playing state."""
        print("Exited Playing State")
        # Clean up sprite groups
        if self.updatable:
            self.updatable.empty()
        if self.drawable:
            self.drawable.empty()
        if self.asteroids:
            self.asteroids.empty()
        if self.shots:
            self.shots.empty()
    
    def update(self, dt):
        """Update game logic."""
        # Update all updatable objects
        self.updatable.update(dt)
        
        # Check collisions
        for asteroid in self.asteroids:
            if asteroid.isColliding(self.player):
                print("Game over!")
                # For now, just return to menu - later this will be handled by lives system
                from menustate import MenuState
                self.state_manager.change_state(MenuState(self.state_manager))
                return
            
            for shot in self.shots:
                if asteroid.isColliding(shot):
                    asteroid.split()
                    shot.kill()
    
    def draw(self, screen):
        """Draw the game to the screen."""
        screen.fill("black")
        
        # Draw all drawable objects
        for drawable_obj in self.drawable:
            drawable_obj.draw(screen)
    
    def handle_event(self, event):
        """Handle playing state events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to menu when ESC is pressed
                from menustate import MenuState
                self.state_manager.change_state(MenuState(self.state_manager))