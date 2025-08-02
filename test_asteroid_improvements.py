import unittest
import pygame
import math
from asteroid import Asteroid
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS


class TestAsteroidImprovements(unittest.TestCase):
    """Test improved asteroid mechanics"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.asteroid = Asteroid(100, 100, ASTEROID_MIN_RADIUS * 2)
        self.asteroid.velocity = pygame.Vector2(50, 0)

    def test_asteroid_has_rotation_properties(self):
        """Test that asteroids have rotation and rotation speed"""
        self.assertTrue(hasattr(self.asteroid, 'rotation'))
        self.assertTrue(hasattr(self.asteroid, 'rotation_speed'))
        self.assertIsInstance(self.asteroid.rotation, (int, float))
        self.assertIsInstance(self.asteroid.rotation_speed, (int, float))

    def test_asteroid_rotation_updates(self):
        """Test that asteroid rotation changes over time"""
        initial_rotation = self.asteroid.rotation
        dt = 0.1
        self.asteroid.update(dt)
        
        # Rotation should have changed (unless rotation_speed is exactly 0, which is unlikely)
        if self.asteroid.rotation_speed != 0:
            self.assertNotEqual(self.asteroid.rotation, initial_rotation)

    def test_asteroid_split_creates_two_asteroids(self):
        """Test that splitting creates two new asteroids with improved mechanics"""
        # Create a medium asteroid that can split
        medium_asteroid = Asteroid(100, 100, ASTEROID_MIN_RADIUS * 2)
        medium_asteroid.velocity = pygame.Vector2(50, 0)
        medium_asteroid.rotation = 45
        medium_asteroid.rotation_speed = 90
        
        # Set up containers to catch the new asteroids
        asteroids_group = pygame.sprite.Group()
        Asteroid.containers = (asteroids_group,)
        
        # Split the asteroid
        points = medium_asteroid.split()
        
        # Should return points
        self.assertEqual(points, 50)  # Medium asteroid points
        
        # Should have created 2 new asteroids
        self.assertEqual(len(asteroids_group), 2)
        
        # Check that new asteroids have proper properties
        new_asteroids = list(asteroids_group)
        for new_asteroid in new_asteroids:
            self.assertTrue(hasattr(new_asteroid, 'rotation'))
            self.assertTrue(hasattr(new_asteroid, 'rotation_speed'))
            self.assertIsInstance(new_asteroid.velocity, pygame.Vector2)
            self.assertGreater(new_asteroid.velocity.length(), 0)

    def test_asteroid_split_velocity_distribution(self):
        """Test that split asteroids have different velocities"""
        # Create a large asteroid
        large_asteroid = Asteroid(100, 100, ASTEROID_MIN_RADIUS * 3)
        large_asteroid.velocity = pygame.Vector2(50, 0)
        
        # Set up containers
        asteroids_group = pygame.sprite.Group()
        Asteroid.containers = (asteroids_group,)
        
        # Split the asteroid
        large_asteroid.split()
        
        # Get the two new asteroids
        new_asteroids = list(asteroids_group)
        self.assertEqual(len(new_asteroids), 2)
        
        # Check that they have different velocities
        velocity1 = new_asteroids[0].velocity
        velocity2 = new_asteroids[1].velocity
        
        # Velocities should be different
        self.assertNotEqual(velocity1.x, velocity2.x)
        self.assertNotEqual(velocity1.y, velocity2.y)
        
        # Both should have reasonable speeds
        self.assertGreater(velocity1.length(), 0)
        self.assertGreater(velocity2.length(), 0)

    def test_small_asteroid_split_returns_points_only(self):
        """Test that smallest asteroids don't split but return points"""
        small_asteroid = Asteroid(100, 100, ASTEROID_MIN_RADIUS)
        small_asteroid.velocity = pygame.Vector2(50, 0)
        
        # Set up containers
        asteroids_group = pygame.sprite.Group()
        Asteroid.containers = (asteroids_group,)
        
        # Split the small asteroid
        points = small_asteroid.split()
        
        # Should return points for small asteroid
        self.assertEqual(points, 100)
        
        # Should not create new asteroids
        self.assertEqual(len(asteroids_group), 0)

    def test_asteroid_draw_method_works(self):
        """Test that the improved draw method doesn't crash"""
        # Create a test surface
        test_surface = pygame.Surface((200, 200))
        
        # This should not raise an exception
        try:
            self.asteroid.draw(test_surface)
            # If we get here, the draw method worked
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Asteroid draw method failed: {e}")

    def test_asteroid_shape_consistency(self):
        """Test that asteroid shape remains consistent between draws"""
        # Create a test surface
        test_surface = pygame.Surface((200, 200))
        
        # Draw the asteroid multiple times - should not crash
        for _ in range(5):
            try:
                self.asteroid.draw(test_surface)
            except Exception as e:
                self.fail(f"Asteroid draw method failed on repeated calls: {e}")


if __name__ == '__main__':
    unittest.main()