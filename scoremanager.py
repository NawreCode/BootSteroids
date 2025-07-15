"""
ScoreManager class for handling scoring logic and high score persistence.
"""
import json
import os
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS


class ScoreManager:
    """Manages scoring, high scores, and extra life milestones."""
    
    # Point values for different asteroid sizes
    LARGE_ASTEROID_POINTS = 20
    MEDIUM_ASTEROID_POINTS = 50
    SMALL_ASTEROID_POINTS = 100
    
    # Extra life milestone
    EXTRA_LIFE_THRESHOLD = 10000
    
    def __init__(self, high_score_file="high_score.json"):
        """Initialize the score manager."""
        self.current_score = 0
        self.high_score = 0
        self.last_extra_life_score = 0
        self.high_score_file = high_score_file
        self.load_high_score()
    
    def add_score(self, points):
        """Add points to the current score."""
        if points < 0:
            raise ValueError("Points cannot be negative")
        
        self.current_score += points
    
    def get_score(self):
        """Get the current score."""
        return self.current_score
    
    def get_high_score(self):
        """Get the high score."""
        return self.high_score
    
    def reset_score(self):
        """Reset the current score to 0."""
        self.current_score = 0
        self.last_extra_life_score = 0
    
    def get_points_for_asteroid_size(self, radius):
        """Get point value based on asteroid radius."""
        max_radius = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
        
        if radius >= max_radius:
            return self.LARGE_ASTEROID_POINTS
        elif radius >= ASTEROID_MIN_RADIUS * 2:
            return self.MEDIUM_ASTEROID_POINTS
        else:
            return self.SMALL_ASTEROID_POINTS
    
    def check_extra_life(self):
        """Check if player has earned an extra life and update milestone."""
        if self.current_score >= self.last_extra_life_score + self.EXTRA_LIFE_THRESHOLD:
            self.last_extra_life_score = (self.current_score // self.EXTRA_LIFE_THRESHOLD) * self.EXTRA_LIFE_THRESHOLD
            return True
        return False
    
    def is_new_high_score(self):
        """Check if current score is a new high score."""
        return self.current_score > self.high_score
    
    def save_high_score(self):
        """Save the high score to file if current score is higher."""
        if self.is_new_high_score():
            self.high_score = self.current_score
            
        try:
            score_data = {
                "high_score": self.high_score
            }
            with open(self.high_score_file, 'w') as f:
                json.dump(score_data, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Warning: Could not save high score: {e}")
    
    def load_high_score(self):
        """Load the high score from file."""
        try:
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, 'r') as f:
                    score_data = json.load(f)
                    self.high_score = score_data.get("high_score", 0)
                    
                    # Validate loaded data
                    if not isinstance(self.high_score, int) or self.high_score < 0:
                        print("Warning: Invalid high score data, resetting to 0")
                        self.high_score = 0
            else:
                self.high_score = 0
        except (IOError, OSError, json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Could not load high score: {e}")
            self.high_score = 0