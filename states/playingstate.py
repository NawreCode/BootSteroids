"""
PlayingState class for active gameplay.
"""
import pygame
from states.gamestate import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS, ASTEROID_KINDS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scoremanager import ScoreManager
from livesmanager import LivesManager
from particle import ParticleSystem


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
        self.particle_system = None
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
        self.particle_system = ParticleSystem()
        
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
        
        # Update particle system
        if self.particle_system:
            self.particle_system.update(dt)
        
        # Check collisions
        for asteroid in self.asteroids:
            if asteroid.isColliding(self.player) and not self.lives_manager.is_invincible():
                print("Player hit! Lives remaining:", self.lives_manager.get_lives() - 1)
                
                # Create player destruction explosion effect
                self.particle_system.emit_explosion(
                    self.player.position,
                    count=30,
                    size="medium",
                    color_scheme="white"
                )
                
                # Add additional burst effect in player's movement direction
                if hasattr(self.player, 'velocity') and self.player.velocity.length() > 0:
                    self.particle_system.emit_burst(
                        self.player.position,
                        self.player.velocity,
                        count=15,
                        spread_angle=3.14159/2,  # 90 degrees
                        color=(255, 100, 100),  # Red color
                        speed_range=(50, 150),
                        lifetime_range=(0.8, 1.5)
                    )
                
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
                    # Create explosion effect based on asteroid size
                    explosion_size = "small"
                    explosion_count = 15
                    
                    # Determine explosion size based on asteroid radius
                    max_radius = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
                    if asteroid.radius >= max_radius:
                        explosion_size = "large"
                        explosion_count = 25
                    elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                        explosion_size = "medium"
                        explosion_count = 20
                    
                    # Create explosion at asteroid position
                    self.particle_system.emit_explosion(
                        asteroid.position, 
                        count=explosion_count, 
                        size=explosion_size, 
                        color_scheme="orange"
                    )
                    
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
        
        # Create respawn particle effect
        respawn_position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # Create a circular burst of particles for respawn effect
        self.particle_system.emit_explosion(
            respawn_position,
            count=20,
            size="small",
            color_scheme="blue"
        )
        
        # Add additional sparkle effect
        import math
        for i in range(12):  # Create 12 particles in a circle
            angle = (i / 12) * 2 * math.pi
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            self.particle_system.emit_burst(
                respawn_position,
                direction,
                count=3,
                spread_angle=math.pi/6,  # 30 degrees
                color=(100, 200, 255),  # Light blue
                speed_range=(80, 120),
                lifetime_range=(1.0, 1.8)
            )
        
        print(f"Player respawned! Invincible for {self.lives_manager.invincibility_duration} seconds")
    
    def _create_invincibility_effects(self):
        """Create subtle particle effects around the player during invincibility."""
        import random
        import math
        
        # Create occasional sparkle particles around the player
        if random.random() < 0.3:  # 30% chance each frame
            # Create particles in a circle around the player
            angle = random.uniform(0, 2 * math.pi)
            distance = self.player.radius + random.uniform(5, 15)
            
            particle_pos = pygame.Vector2(
                self.player.position.x + math.cos(angle) * distance,
                self.player.position.y + math.sin(angle) * distance
            )
            
            # Create a small sparkle effect
            sparkle_velocity = pygame.Vector2(
                random.uniform(-20, 20),
                random.uniform(-20, 20)
            )
            
            # Use light blue/white colors for invincibility
            colors = [(200, 200, 255), (255, 255, 255), (150, 200, 255)]
            color = random.choice(colors)
            
            from particle import Particle
            particle = Particle(
                particle_pos,
                sparkle_velocity,
                color,
                lifetime=0.8,
                size=1
            )
            self.particle_system.particles.append(particle)
    
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
                
                # Add invincibility particle effects around the player
                self._create_invincibility_effects()
            else:
                drawable_obj.draw(screen)
        
        # Draw particle effects
        if self.particle_system:
            self.particle_system.draw(screen)
        
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