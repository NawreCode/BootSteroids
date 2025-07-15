"""
Unit tests for ScoreManager class.
"""
import unittest
import os
import json
import tempfile
from scoremanager import ScoreManager
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS


class TestScoreManager(unittest.TestCase):
    """Test cases for ScoreManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.score_manager = ScoreManager(high_score_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_initial_state(self):
        """Test initial state of ScoreManager."""
        self.assertEqual(self.score_manager.get_score(), 0)
        self.assertEqual(self.score_manager.get_high_score(), 0)
        self.assertEqual(self.score_manager.last_extra_life_score, 0)
    
    def test_add_score(self):
        """Test adding score."""
        self.score_manager.add_score(100)
        self.assertEqual(self.score_manager.get_score(), 100)
        
        self.score_manager.add_score(50)
        self.assertEqual(self.score_manager.get_score(), 150)
    
    def test_add_negative_score_raises_error(self):
        """Test that adding negative score raises ValueError."""
        with self.assertRaises(ValueError):
            self.score_manager.add_score(-10)
    
    def test_reset_score(self):
        """Test resetting score."""
        self.score_manager.add_score(500)
        self.score_manager.reset_score()
        self.assertEqual(self.score_manager.get_score(), 0)
        self.assertEqual(self.score_manager.last_extra_life_score, 0)
    
    def test_asteroid_point_values(self):
        """Test point values for different asteroid sizes."""
        # Large asteroid (max radius)
        max_radius = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
        self.assertEqual(
            self.score_manager.get_points_for_asteroid_size(max_radius),
            ScoreManager.LARGE_ASTEROID_POINTS
        )
        
        # Medium asteroid
        medium_radius = ASTEROID_MIN_RADIUS * 2
        self.assertEqual(
            self.score_manager.get_points_for_asteroid_size(medium_radius),
            ScoreManager.MEDIUM_ASTEROID_POINTS
        )
        
        # Small asteroid
        small_radius = ASTEROID_MIN_RADIUS
        self.assertEqual(
            self.score_manager.get_points_for_asteroid_size(small_radius),
            ScoreManager.SMALL_ASTEROID_POINTS
        )
    
    def test_extra_life_milestone(self):
        """Test extra life milestone checking."""
        # No extra life at start
        self.assertFalse(self.score_manager.check_extra_life())
        
        # Add score just below threshold
        self.score_manager.add_score(9999)
        self.assertFalse(self.score_manager.check_extra_life())
        
        # Add score to reach threshold
        self.score_manager.add_score(1)
        self.assertTrue(self.score_manager.check_extra_life())
        
        # Should not trigger again until next milestone
        self.score_manager.add_score(1000)
        self.assertFalse(self.score_manager.check_extra_life())
        
        # Trigger next milestone
        self.score_manager.add_score(9000)  # Total: 20000
        self.assertTrue(self.score_manager.check_extra_life())
    
    def test_high_score_detection(self):
        """Test high score detection."""
        # Initially no high score
        self.assertFalse(self.score_manager.is_new_high_score())
        
        # Add score to create high score
        self.score_manager.add_score(1000)
        self.assertTrue(self.score_manager.is_new_high_score())
    
    def test_high_score_persistence(self):
        """Test saving and loading high scores."""
        # Set a high score and save
        self.score_manager.add_score(5000)
        self.score_manager.save_high_score()
        
        # Create new manager with same file
        new_manager = ScoreManager(high_score_file=self.temp_file.name)
        self.assertEqual(new_manager.get_high_score(), 5000)
    
    def test_high_score_file_corruption_handling(self):
        """Test handling of corrupted high score file."""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json")
        
        # Should handle gracefully and default to 0
        manager = ScoreManager(high_score_file=self.temp_file.name)
        self.assertEqual(manager.get_high_score(), 0)
    
    def test_invalid_high_score_data_handling(self):
        """Test handling of invalid high score data."""
        # Write invalid high score value
        with open(self.temp_file.name, 'w') as f:
            json.dump({"high_score": "invalid"}, f)
        
        # Should handle gracefully and default to 0
        manager = ScoreManager(high_score_file=self.temp_file.name)
        self.assertEqual(manager.get_high_score(), 0)
    
    def test_missing_high_score_file(self):
        """Test handling of missing high score file."""
        # Use non-existent file
        manager = ScoreManager(high_score_file="nonexistent.json")
        self.assertEqual(manager.get_high_score(), 0)


if __name__ == '__main__':
    unittest.main()