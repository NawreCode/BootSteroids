import unittest
import pygame
from player import Player
from asteroid import Asteroid
from shot import Shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, ASTEROID_MIN_RADIUS, SHOT_RADIUS


class TestScreenWrapping(unittest.TestCase):
    """Test screen wrapping functionality for all game objects"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.player = Player(100, 100)
        self.asteroid = Asteroid(100, 100, ASTEROID_MIN_RADIUS)
        self.shot = Shot(100, 100)

    def test_player_wrap_left_edge(self):
        """Test player wrapping from left edge to right edge"""
        self.player.position.x = -1
        self.player.wrap_screen()
        self.assertEqual(self.player.position.x, SCREEN_WIDTH)

    def test_player_wrap_right_edge(self):
        """Test player wrapping from right edge to left edge"""
        self.player.position.x = SCREEN_WIDTH + 1
        self.player.wrap_screen()
        self.assertEqual(self.player.position.x, 0)

    def test_player_wrap_top_edge(self):
        """Test player wrapping from top edge to bottom edge"""
        self.player.position.y = -1
        self.player.wrap_screen()
        self.assertEqual(self.player.position.y, SCREEN_HEIGHT)

    def test_player_wrap_bottom_edge(self):
        """Test player wrapping from bottom edge to top edge"""
        self.player.position.y = SCREEN_HEIGHT + 1
        self.player.wrap_screen()
        self.assertEqual(self.player.position.y, 0)

    def test_player_no_wrap_inside_screen(self):
        """Test player doesn't wrap when inside screen bounds"""
        original_x = 100
        original_y = 100
        self.player.position.x = original_x
        self.player.position.y = original_y
        self.player.wrap_screen()
        self.assertEqual(self.player.position.x, original_x)
        self.assertEqual(self.player.position.y, original_y)

    def test_asteroid_wrap_left_edge(self):
        """Test asteroid wrapping from left edge to right edge"""
        self.asteroid.position.x = -1
        self.asteroid.wrap_screen()
        self.assertEqual(self.asteroid.position.x, SCREEN_WIDTH)

    def test_asteroid_wrap_right_edge(self):
        """Test asteroid wrapping from right edge to left edge"""
        self.asteroid.position.x = SCREEN_WIDTH + 1
        self.asteroid.wrap_screen()
        self.assertEqual(self.asteroid.position.x, 0)

    def test_asteroid_wrap_top_edge(self):
        """Test asteroid wrapping from top edge to bottom edge"""
        self.asteroid.position.y = -1
        self.asteroid.wrap_screen()
        self.assertEqual(self.asteroid.position.y, SCREEN_HEIGHT)

    def test_asteroid_wrap_bottom_edge(self):
        """Test asteroid wrapping from bottom edge to top edge"""
        self.asteroid.position.y = SCREEN_HEIGHT + 1
        self.asteroid.wrap_screen()
        self.assertEqual(self.asteroid.position.y, 0)

    def test_asteroid_no_wrap_inside_screen(self):
        """Test asteroid doesn't wrap when inside screen bounds"""
        original_x = 100
        original_y = 100
        self.asteroid.position.x = original_x
        self.asteroid.position.y = original_y
        self.asteroid.wrap_screen()
        self.assertEqual(self.asteroid.position.x, original_x)
        self.assertEqual(self.asteroid.position.y, original_y)

    def test_shot_wrap_left_edge(self):
        """Test shot wrapping from left edge to right edge"""
        self.shot.position.x = -1
        self.shot.wrap_screen()
        self.assertEqual(self.shot.position.x, SCREEN_WIDTH)

    def test_shot_wrap_right_edge(self):
        """Test shot wrapping from right edge to left edge"""
        self.shot.position.x = SCREEN_WIDTH + 1
        self.shot.wrap_screen()
        self.assertEqual(self.shot.position.x, 0)

    def test_shot_wrap_top_edge(self):
        """Test shot wrapping from top edge to bottom edge"""
        self.shot.position.y = -1
        self.shot.wrap_screen()
        self.assertEqual(self.shot.position.y, SCREEN_HEIGHT)

    def test_shot_wrap_bottom_edge(self):
        """Test shot wrapping from bottom edge to top edge"""
        self.shot.position.y = SCREEN_HEIGHT + 1
        self.shot.wrap_screen()
        self.assertEqual(self.shot.position.y, 0)

    def test_shot_no_wrap_inside_screen(self):
        """Test shot doesn't wrap when inside screen bounds"""
        original_x = 100
        original_y = 100
        self.shot.position.x = original_x
        self.shot.position.y = original_y
        self.shot.wrap_screen()
        self.assertEqual(self.shot.position.x, original_x)
        self.assertEqual(self.shot.position.y, original_y)

    def test_wrapping_integration_with_update(self):
        """Test that wrapping is called during update methods"""
        # Test player update calls wrapping
        self.player.position.x = -1
        self.player.update(0.1)  # Small dt to avoid other movement
        self.assertEqual(self.player.position.x, SCREEN_WIDTH)

        # Test asteroid update calls wrapping
        self.asteroid.position.x = -1
        self.asteroid.velocity = pygame.Vector2(0, 0)  # No movement
        self.asteroid.update(0.1)
        self.assertEqual(self.asteroid.position.x, SCREEN_WIDTH)

        # Test shot update calls wrapping
        self.shot.position.x = -1
        self.shot.velocity = pygame.Vector2(0, 0)  # No movement
        self.shot.update(0.1)
        self.assertEqual(self.shot.position.x, SCREEN_WIDTH)


if __name__ == '__main__':
    unittest.main()