"""
PlayingState class for active gameplay.
"""
import pygame
from states.gamestate import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scoremanager import ScoreManager
from livesmanager import LivesManager


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
        self.score_manager = None
        self.lives_manager = None
        self.extra_life_notification_time = 0
        self.extra_life_notification_duration = 3.0  # Show notification for 3 seconds
    
    def enter(self):
        """Called when entering the playing state."""
        print("Entered Playing State")
        
        # Initialize sprite groups
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Initialize managers
        self.score_manager = ScoreManager()
        self.lives_manager = LivesManager()
        
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
            if asteroid.isColliding(self.player) and not self.lives_manager.is_invincible():
                print("Player hit! Lives remaining:", self.lives_manager.get_lives() - 1)
                
                # Lose a life and check if game over
                game_over = self.lives_manager.lose_life()
                
                if game_over:
                    print("Game over!")
                    # Save high score before transitioning
                    self.score_manager.save_high_score()
                    # Transition to game over state with final score
                    from states.gameoverstate import GameOverState
                    self.state_manager.change_state(GameOverState(self.state_manager, final_score=self.score_manager.get_score()))
                    return
                else:
                    # Respawn player at center
                    self.respawn_player()
                    break  # Exit collision loop to prevent multiple hits
            
            for shot in self.shots:
                if asteroid.isColliding(shot):
                    # Award points for destroying asteroid
                    points = asteroid.split()
                    self.score_manager.add_score(points)
                    
                    # Check for extra life milestone
                    if self.score_manager.check_extra_life():
                        self.lives_manager.add_life()
                        print(f"Extra life earned! Lives: {self.lives_manager.get_lives()}")
                        # Store the extra life notification for visual display
                        self.show_extra_life_notification()
                    
                    shot.kill()
    
    def respawn_player(self):
        """Respawn the player at the center of the screen."""
        # Reset player position to center
        self.player.position.x = SCREEN_WIDTH / 2
        self.player.position.y = SCREEN_HEIGHT / 2
        # Reset player rotation
        self.player.rotation = 0
        print(f"Player respawned! Invincible for {self.lives_manager.invincibility_duration} seconds")
    
    def show_extra_life_notification(self):
        """Show extra life notification for a few seconds."""
        import time
        self.extra_life_notification_time = time.time()
    
    def draw(self, screen):
        """Draw the game to the screen."""
        screen.fill("black")
        
        # Draw all drawable objects with invincibility flashing effect
        for drawable_obj in self.drawable:
            # Check if this is the player and if they're invincible
            if drawable_obj == self.player and self.lives_manager.is_invincible():
                # Create flashing effect by skipping drawing every few frames
                import time
                flash_rate = 8  # flashes per second
                if int(time.time() * flash_rate) % 2 == 0:
                    drawable_obj.draw(screen)
            else:
                drawable_obj.draw(screen)
        
        # Draw UI elements
        if self.score_manager and self.lives_manager:
            font = pygame.font.Font(None, 36)
            
            # Draw score
            score_text = font.render(f"Score: {self.score_manager.get_score()}", True, "white")
            screen.blit(score_text, (10, 10))
            
            # Draw high score
            high_score_text = font.render(f"High Score: {self.score_manager.get_high_score()}", True, "white")
            screen.blit(high_score_text, (10, 50))
            
            # Draw lives
            lives_text = font.render(f"Lives: {self.lives_manager.get_lives()}", True, "white")
            screen.blit(lives_text, (10, 90))
            
            # Draw invincibility indicator if active
            if self.lives_manager.is_invincible():
                remaining_time = self.lives_manager.get_invincibility_time_remaining()
                invincible_text = font.render(f"Invincible: {remaining_time:.1f}s", True, "yellow")
                screen.blit(invincible_text, (10, 130))
            
            # Draw extra life notification if active
            import time
            import math
            if self.extra_life_notification_time > 0:
                elapsed_time = time.time() - self.extra_life_notification_time
                if elapsed_time < self.extra_life_notification_duration:
                    # Create pulsing effect for extra life notification
                    pulse_intensity = abs(math.sin(elapsed_time * 4))
                    extra_life_font = pygame.font.Font(None, 48)
                    
                    # Create color with pulsing effect (bright green to darker green)
                    green_value = int(128 + 127 * pulse_intensity)
                    extra_life_text = extra_life_font.render("EXTRA LIFE!", True, (0, green_value, 0))
                    
                    # Center the notification on screen
                    text_rect = extra_life_text.get_rect()
                    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
                    screen.blit(extra_life_text, text_rect)
                else:
                    # Reset notification time when duration expires
                    self.extra_life_notification_time = 0
    
    def handle_event(self, event):
        """Handle playing state events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Transition to paused state when ESC is pressed
                from states.pausedstate import PausedState
                self.state_manager.change_state(PausedState(self.state_manager, self))