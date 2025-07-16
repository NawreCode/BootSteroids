"""
LivesManager class for handling player lives and invincibility system.
"""
import time


class LivesManager:
    """Manages player lives, respawn logic, and invincibility system."""
    
    # Default configuration
    DEFAULT_INITIAL_LIVES = 3
    DEFAULT_INVINCIBILITY_DURATION = 2.0  # seconds
    
    def __init__(self, initial_lives=None, invincibility_duration=None):
        """Initialize the lives manager."""
        self.initial_lives = initial_lives if initial_lives is not None else self.DEFAULT_INITIAL_LIVES
        self.invincibility_duration = invincibility_duration if invincibility_duration is not None else self.DEFAULT_INVINCIBILITY_DURATION
        
        if self.initial_lives < 0:
            raise ValueError("Initial lives cannot be negative")
        if self.invincibility_duration < 0:
            raise ValueError("Invincibility duration cannot be negative")
        
        self.current_lives = self.initial_lives
        self.invincibility_start_time = 0
        self.is_invincible_active = False
    
    def lose_life(self):
        """
        Reduce lives by 1 and start invincibility period.
        Returns True if game over (no lives remaining), False otherwise.
        """
        if self.current_lives > 0:
            self.current_lives -= 1
            self.start_invincibility()
        
        return self.current_lives <= 0
    
    def add_life(self):
        """Add one life to the current count."""
        self.current_lives += 1
    
    def get_lives(self):
        """Get the current number of lives."""
        return self.current_lives
    
    def reset_lives(self):
        """Reset lives to initial count and clear invincibility."""
        self.current_lives = self.initial_lives
        self.is_invincible_active = False
        self.invincibility_start_time = 0
    
    def start_invincibility(self):
        """Start the invincibility period."""
        self.is_invincible_active = True
        self.invincibility_start_time = time.time()
    
    def is_invincible(self):
        """
        Check if player is currently invincible.
        Updates invincibility status based on elapsed time.
        """
        if not self.is_invincible_active:
            return False
        
        elapsed_time = time.time() - self.invincibility_start_time
        if elapsed_time >= self.invincibility_duration:
            self.is_invincible_active = False
            return False
        
        return True
    
    def get_invincibility_time_remaining(self):
        """
        Get remaining invincibility time in seconds.
        Returns 0 if not invincible.
        """
        if not self.is_invincible_active:
            return 0
        
        elapsed_time = time.time() - self.invincibility_start_time
        remaining = self.invincibility_duration - elapsed_time
        return max(0, remaining)
    
    def is_game_over(self):
        """Check if the game is over (no lives remaining)."""
        return self.current_lives <= 0