"""
Unit tests for LivesManager class.
"""
import pytest
import time
from livesmanager import LivesManager


class TestLivesManager:
    """Test cases for LivesManager class."""
    
    def test_initialization_default_values(self):
        """Test LivesManager initialization with default values."""
        lives_manager = LivesManager()
        
        assert lives_manager.get_lives() == 3
        assert lives_manager.initial_lives == 3
        assert lives_manager.invincibility_duration == 2.0
        assert not lives_manager.is_invincible()
        assert not lives_manager.is_game_over()
    
    def test_initialization_custom_values(self):
        """Test LivesManager initialization with custom values."""
        lives_manager = LivesManager(initial_lives=5, invincibility_duration=3.0)
        
        assert lives_manager.get_lives() == 5
        assert lives_manager.initial_lives == 5
        assert lives_manager.invincibility_duration == 3.0
    
    def test_initialization_invalid_values(self):
        """Test LivesManager initialization with invalid values."""
        with pytest.raises(ValueError, match="Initial lives cannot be negative"):
            LivesManager(initial_lives=-1)
        
        with pytest.raises(ValueError, match="Invincibility duration cannot be negative"):
            LivesManager(invincibility_duration=-1.0)
    
    def test_lose_life_normal_case(self):
        """Test losing a life in normal circumstances."""
        lives_manager = LivesManager(initial_lives=3)
        
        # Lose first life
        game_over = lives_manager.lose_life()
        assert not game_over
        assert lives_manager.get_lives() == 2
        assert lives_manager.is_invincible()
        
        # Lose second life
        game_over = lives_manager.lose_life()
        assert not game_over
        assert lives_manager.get_lives() == 1
        
        # Lose last life
        game_over = lives_manager.lose_life()
        assert game_over
        assert lives_manager.get_lives() == 0
        assert lives_manager.is_game_over()
    
    def test_lose_life_when_no_lives_remaining(self):
        """Test losing a life when already at 0 lives."""
        lives_manager = LivesManager(initial_lives=1)
        
        # Lose the only life
        game_over = lives_manager.lose_life()
        assert game_over
        assert lives_manager.get_lives() == 0
        
        # Try to lose another life when already at 0
        game_over = lives_manager.lose_life()
        assert game_over
        assert lives_manager.get_lives() == 0
    
    def test_add_life(self):
        """Test adding lives."""
        lives_manager = LivesManager(initial_lives=3)
        
        lives_manager.add_life()
        assert lives_manager.get_lives() == 4
        
        lives_manager.add_life()
        assert lives_manager.get_lives() == 5
    
    def test_reset_lives(self):
        """Test resetting lives to initial count."""
        lives_manager = LivesManager(initial_lives=3)
        
        # Modify state
        lives_manager.lose_life()
        lives_manager.add_life()
        assert lives_manager.get_lives() == 3
        assert lives_manager.is_invincible()
        
        # Reset
        lives_manager.reset_lives()
        assert lives_manager.get_lives() == 3
        assert not lives_manager.is_invincible()
    
    def test_invincibility_system(self):
        """Test invincibility system timing."""
        lives_manager = LivesManager(initial_lives=3, invincibility_duration=0.1)
        
        # Initially not invincible
        assert not lives_manager.is_invincible()
        assert lives_manager.get_invincibility_time_remaining() == 0
        
        # Start invincibility
        lives_manager.start_invincibility()
        assert lives_manager.is_invincible()
        assert lives_manager.get_invincibility_time_remaining() > 0
        
        # Wait for invincibility to expire
        time.sleep(0.15)
        assert not lives_manager.is_invincible()
        assert lives_manager.get_invincibility_time_remaining() == 0
    
    def test_invincibility_after_losing_life(self):
        """Test that invincibility starts automatically after losing a life."""
        lives_manager = LivesManager(initial_lives=2, invincibility_duration=0.1)
        
        assert not lives_manager.is_invincible()
        
        lives_manager.lose_life()
        assert lives_manager.is_invincible()
        assert lives_manager.get_invincibility_time_remaining() > 0
        
        # Wait for invincibility to expire
        time.sleep(0.15)
        assert not lives_manager.is_invincible()
    
    def test_game_over_conditions(self):
        """Test game over detection."""
        lives_manager = LivesManager(initial_lives=1)
        
        assert not lives_manager.is_game_over()
        
        lives_manager.lose_life()
        assert lives_manager.is_game_over()
    
    def test_invincibility_time_remaining_accuracy(self):
        """Test invincibility time remaining calculation."""
        lives_manager = LivesManager(initial_lives=3, invincibility_duration=1.0)
        
        lives_manager.start_invincibility()
        
        # Check that time remaining decreases
        initial_time = lives_manager.get_invincibility_time_remaining()
        assert 0.9 <= initial_time <= 1.0
        
        time.sleep(0.1)
        later_time = lives_manager.get_invincibility_time_remaining()
        assert later_time < initial_time
    
    def test_multiple_invincibility_periods(self):
        """Test multiple invincibility periods don't overlap incorrectly."""
        lives_manager = LivesManager(initial_lives=3, invincibility_duration=0.1)
        
        # First invincibility period
        lives_manager.start_invincibility()
        assert lives_manager.is_invincible()
        
        time.sleep(0.15)
        assert not lives_manager.is_invincible()
        
        # Second invincibility period
        lives_manager.start_invincibility()
        assert lives_manager.is_invincible()
        
        time.sleep(0.15)
        assert not lives_manager.is_invincible()
    
    def test_edge_case_zero_initial_lives(self):
        """Test edge case with zero initial lives."""
        lives_manager = LivesManager(initial_lives=0)
        
        assert lives_manager.get_lives() == 0
        assert lives_manager.is_game_over()
        
        # Losing a life when already at 0
        game_over = lives_manager.lose_life()
        assert game_over
        assert lives_manager.get_lives() == 0
        
        # Adding a life should make game not over
        lives_manager.add_life()
        assert lives_manager.get_lives() == 1
        assert not lives_manager.is_game_over()
    
    def test_edge_case_zero_invincibility_duration(self):
        """Test edge case with zero invincibility duration."""
        lives_manager = LivesManager(initial_lives=3, invincibility_duration=0.0)
        
        lives_manager.start_invincibility()
        # With 0 duration, should not be invincible
        assert not lives_manager.is_invincible()
        assert lives_manager.get_invincibility_time_remaining() == 0