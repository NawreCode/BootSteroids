import unittest
import unittest.mock
import pygame
from player import Player
from constants import PLAYER_RADIUS, PLAYER_ACCELERATION, PLAYER_DRAG, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED


class TestPlayerImprovements(unittest.TestCase):
    """Test improved player mechanics"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.player = Player(100, 100)

    def test_player_has_velocity_property(self):
        """Test that player has velocity for momentum system"""
        self.assertTrue(hasattr(self.player, 'velocity'))
        self.assertIsInstance(self.player.velocity, pygame.Vector2)
        self.assertEqual(self.player.velocity.x, 0)
        self.assertEqual(self.player.velocity.y, 0)

    def test_player_thrust_increases_velocity(self):
        """Test that thrusting increases player velocity"""
        initial_velocity = self.player.velocity.copy()
        dt = 0.1
        
        # Apply forward thrust
        self.player.thrust(dt, 1)
        
        # Velocity should have increased
        self.assertNotEqual(self.player.velocity, initial_velocity)
        self.assertGreater(self.player.velocity.length(), 0)

    def test_player_backward_thrust(self):
        """Test that backward thrust works correctly"""
        dt = 0.1
        
        # Apply forward thrust first
        self.player.thrust(dt, 1)
        forward_velocity = self.player.velocity.copy()
        
        # Apply backward thrust
        self.player.thrust(dt, -1)
        
        # Velocity should be different (reduced or reversed)
        self.assertNotEqual(self.player.velocity, forward_velocity)

    def test_player_drag_reduces_velocity(self):
        """Test that drag reduces player velocity over time"""
        dt = 0.1
        
        # Give player some initial velocity
        self.player.velocity = pygame.Vector2(100, 0)
        initial_speed = self.player.velocity.length()
        
        # Update player (which applies drag)
        self.player.update(dt)
        
        # Velocity should be reduced due to drag
        final_speed = self.player.velocity.length()
        self.assertLess(final_speed, initial_speed)

    def test_player_momentum_affects_position(self):
        """Test that player momentum affects position"""
        initial_position = self.player.position.copy()
        dt = 0.1
        
        # Give player some velocity
        self.player.velocity = pygame.Vector2(50, 0)
        
        # Update player
        self.player.update(dt)
        
        # Position should have changed based on velocity
        self.assertNotEqual(self.player.position, initial_position)
        self.assertGreater(self.player.position.x, initial_position.x)

    def test_shooting_cooldown_prevents_rapid_fire(self):
        """Test that shooting cooldown prevents rapid-fire abuse"""
        # Set up sprite groups for shots
        shots_group = pygame.sprite.Group()
        from shot import Shot
        Shot.containers = (shots_group,)
        
        # Reset cooldown
        self.player.shoot_cooldown = 0
        
        # First shot should work
        self.player.shoot()
        self.assertGreater(self.player.shoot_cooldown, 0)
        first_shot_count = len(shots_group)
        
        # Immediate second shot should be blocked
        self.player.shoot()
        second_shot_count = len(shots_group)
        
        # Should not have created another shot
        self.assertEqual(first_shot_count, second_shot_count)

    def test_shooting_cooldown_allows_shot_after_time(self):
        """Test that shooting works again after cooldown expires"""
        # Set up sprite groups for shots
        shots_group = pygame.sprite.Group()
        from shot import Shot
        Shot.containers = (shots_group,)
        
        # Reset cooldown
        self.player.shoot_cooldown = 0
        
        # First shot
        self.player.shoot()
        first_shot_count = len(shots_group)
        
        # Simulate time passing
        self.player.shoot_cooldown = 0  # Reset cooldown manually
        
        # Second shot should work now
        self.player.shoot()
        second_shot_count = len(shots_group)
        
        # Should have created another shot
        self.assertGreater(second_shot_count, first_shot_count)

    def test_shot_velocity_uses_correct_constant(self):
        """Test that shots use the corrected PLAYER_SHOOT_SPEED constant"""
        # Set up sprite groups for shots
        shots_group = pygame.sprite.Group()
        from shot import Shot
        Shot.containers = (shots_group,)
        
        # Reset cooldown and shoot
        self.player.shoot_cooldown = 0
        self.player.rotation = 0  # Point upward
        self.player.shoot()
        
        # Get the shot that was created
        shots = list(shots_group)
        self.assertEqual(len(shots), 1)
        
        shot = shots[0]
        # Shot velocity should match the expected speed
        expected_speed = PLAYER_SHOOT_SPEED
        actual_speed = shot.velocity.length()
        
        # Allow for small floating point differences
        self.assertAlmostEqual(actual_speed, expected_speed, places=1)

    def test_player_rotation_still_works(self):
        """Test that player rotation mechanics still work correctly"""
        initial_rotation = self.player.rotation
        dt = 0.1
        
        # Rotate the player
        self.player.rotate(dt)
        
        # Rotation should have changed
        self.assertNotEqual(self.player.rotation, initial_rotation)

    def test_momentum_system_integration(self):
        """Test that the complete momentum system works together"""
        dt = 1/60  # 60 FPS
        initial_position = self.player.position.copy()
        
        # Apply thrust for several frames using the player's update method
        # Simulate pressing the thrust key
        with unittest.mock.patch('pygame.key.get_pressed') as mock_keys:
            mock_keys.return_value = {pygame.K_z: True, pygame.K_q: False, pygame.K_d: False, 
                                    pygame.K_s: False, pygame.K_SPACE: False}
            
            for _ in range(5):
                self.player.update(dt)
        
        # Player should have moved and have some velocity
        self.assertNotEqual(self.player.position, initial_position)
        self.assertGreater(self.player.velocity.length(), 0)
        
        # Now let drag slow the player down over time (no thrust)
        with unittest.mock.patch('pygame.key.get_pressed') as mock_keys:
            mock_keys.return_value = {pygame.K_z: False, pygame.K_q: False, pygame.K_d: False, 
                                    pygame.K_s: False, pygame.K_SPACE: False}
            
            for _ in range(60):  # 1 second of drag at 60 FPS
                self.player.update(dt)
        
        # Velocity should be much smaller now
        self.assertLess(self.player.velocity.length(), 20)  # Should be quite small after 1 second


if __name__ == '__main__':
    unittest.main()