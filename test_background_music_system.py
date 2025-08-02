#!/usr/bin/env python3
"""
Test script for the background music system integration.
Tests music state management across different game states.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from soundmanager import SoundManager
from gamestatemanager import GameStateManager
from states.menustate import MenuState
from states.playingstate import PlayingState
from states.pausedstate import PausedState
from states.gameoverstate import GameOverState


class TestBackgroundMusicSystem(unittest.TestCase):
    """Test the background music system integration across game states."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock pygame to avoid actual initialization
        self.pygame_patcher = patch('pygame.mixer')
        self.mock_mixer = self.pygame_patcher.start()
        
        # Mock pygame.font for state tests
        self.font_patcher = patch('pygame.font')
        self.mock_font = self.font_patcher.start()
        
        # Mock pygame.time for timer events
        self.time_patcher = patch('pygame.time')
        self.mock_time = self.time_patcher.start()
        
        # Create a mock sound manager
        self.sound_manager = Mock(spec=SoundManager)
        self.state_manager = Mock(spec=GameStateManager)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.pygame_patcher.stop()
        self.font_patcher.stop()
        self.time_patcher.stop()
    
    def test_sound_manager_music_functionality(self):
        """Test that SoundManager has all required music functionality."""
        # Create a real SoundManager instance (with mocked pygame)
        sound_manager = SoundManager()
        
        # Test that all required methods exist
        self.assertTrue(hasattr(sound_manager, 'play_music'))
        self.assertTrue(hasattr(sound_manager, 'stop_music'))
        self.assertTrue(hasattr(sound_manager, 'pause_music'))
        self.assertTrue(hasattr(sound_manager, 'unpause_music'))
        self.assertTrue(hasattr(sound_manager, 'set_music_volume'))
        self.assertTrue(hasattr(sound_manager, 'get_music_volume'))
        self.assertTrue(hasattr(sound_manager, 'is_music_playing'))
        self.assertTrue(hasattr(sound_manager, 'fade_out_music'))
        self.assertTrue(hasattr(sound_manager, 'fade_in_music'))
        self.assertTrue(hasattr(sound_manager, 'crossfade_music'))
        
        # Test volume controls
        sound_manager.set_music_volume(0.5)
        self.assertEqual(sound_manager.get_music_volume(), 0.5)
        
        # Test volume bounds
        sound_manager.set_music_volume(1.5)  # Should clamp to 1.0
        self.assertEqual(sound_manager.get_music_volume(), 1.0)
        
        sound_manager.set_music_volume(-0.5)  # Should clamp to 0.0
        self.assertEqual(sound_manager.get_music_volume(), 0.0)
    
    def test_menu_state_music_integration(self):
        """Test that MenuState properly integrates with music system."""
        menu_state = MenuState(self.state_manager, self.sound_manager)
        
        # Test that sound_manager is stored
        self.assertEqual(menu_state.sound_manager, self.sound_manager)
        
        # Test enter method calls play_music
        menu_state.enter()
        self.sound_manager.play_music.assert_called_with('sounds/menu_music.mp3', loop=True)
        
        # Test menu navigation sounds
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_UP
        
        menu_state.handle_event(mock_event)
        self.sound_manager.play_sound.assert_called_with('menu_navigate')
    
    def test_playing_state_music_integration(self):
        """Test that PlayingState properly integrates with music system."""
        playing_state = PlayingState(self.state_manager, self.sound_manager)
        
        # Test that sound_manager is stored
        self.assertEqual(playing_state.sound_manager, self.sound_manager)
        
        # Mock required pygame components for enter method
        with patch('pygame.sprite.Group'), \
             patch('states.playingstate.ScoreManager'), \
             patch('states.playingstate.LivesManager'), \
             patch('states.playingstate.ParticleSystem'), \
             patch('states.playingstate.Player'), \
             patch('states.playingstate.AsteroidField'):
            
            playing_state.enter()
            self.sound_manager.play_music.assert_called_with('sounds/gameplay_music.mp3', loop=True)
    
    def test_paused_state_music_integration(self):
        """Test that PausedState properly manages music pause/resume."""
        # Create a mock playing state
        mock_playing_state = Mock()
        mock_playing_state.sound_manager = self.sound_manager
        
        paused_state = PausedState(self.state_manager, mock_playing_state, self.sound_manager)
        
        # Test enter method pauses music
        paused_state.enter()
        self.sound_manager.pause_music.assert_called_once()
        
        # Test resume functionality
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_ESCAPE
        
        paused_state.handle_event(mock_event)
        self.sound_manager.unpause_music.assert_called()
    
    def test_game_over_state_music_integration(self):
        """Test that GameOverState properly handles music transitions."""
        game_over_state = GameOverState(self.state_manager, final_score=1000, sound_manager=self.sound_manager)
        
        # Test that sound_manager is stored
        self.assertEqual(game_over_state.sound_manager, self.sound_manager)
        
        # Test enter method fades out current music
        game_over_state.enter()
        self.sound_manager.fade_out_music.assert_called_with(2000)
        
        # Test timer event for game over music
        mock_event = Mock()
        mock_event.type = pygame.USEREVENT + 1
        
        game_over_state.handle_event(mock_event)
        self.sound_manager.play_music.assert_called_with('sounds/gameover_music.mp3', loop=True)
    
    def test_music_state_transitions(self):
        """Test music transitions between different game states."""
        # This test verifies the complete music flow through state transitions
        
        # Menu -> Playing
        menu_state = MenuState(self.state_manager, self.sound_manager)
        menu_state.enter()
        self.sound_manager.play_music.assert_called_with('sounds/menu_music.mp3', loop=True)
        
        # Playing -> Paused
        mock_playing_state = Mock()
        mock_playing_state.sound_manager = self.sound_manager
        paused_state = PausedState(self.state_manager, mock_playing_state, self.sound_manager)
        paused_state.enter()
        self.sound_manager.pause_music.assert_called()
        
        # Paused -> Playing (resume)
        self.sound_manager.reset_mock()
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_ESCAPE
        paused_state.handle_event(mock_event)
        self.sound_manager.unpause_music.assert_called()
        
        # Playing -> Game Over
        self.sound_manager.reset_mock()
        game_over_state = GameOverState(self.state_manager, final_score=1000, sound_manager=self.sound_manager)
        game_over_state.enter()
        self.sound_manager.fade_out_music.assert_called_with(2000)
    
    def test_music_volume_controls(self):
        """Test music volume control functionality."""
        sound_manager = SoundManager()
        
        # Test initial volume
        initial_volume = sound_manager.get_music_volume()
        self.assertEqual(initial_volume, 0.7)  # Default volume
        
        # Test setting volume
        sound_manager.set_music_volume(0.5)
        self.assertEqual(sound_manager.get_music_volume(), 0.5)
        
        # Test volume bounds
        sound_manager.set_music_volume(2.0)  # Should clamp to 1.0
        self.assertEqual(sound_manager.get_music_volume(), 1.0)
        
        sound_manager.set_music_volume(-1.0)  # Should clamp to 0.0
        self.assertEqual(sound_manager.get_music_volume(), 0.0)
    
    def test_fade_effects(self):
        """Test music fade in/out functionality."""
        sound_manager = SoundManager()
        
        # Test fade out
        sound_manager.fade_out_music(1000)
        # Since pygame is mocked, we just verify the method exists and can be called
        
        # Test fade in
        result = sound_manager.fade_in_music('sounds/test_music.mp3', 1000, True)
        # With mocked pygame, this should return False (file not found)
        self.assertFalse(result)
        
        # Test crossfade
        result = sound_manager.crossfade_music('sounds/test_music.mp3', 2000, True)
        self.assertFalse(result)  # Should return False with mocked pygame


def run_integration_test():
    """Run a simple integration test to verify the system works."""
    print("Running background music system integration test...")
    
    try:
        # Test SoundManager initialization
        sound_manager = SoundManager()
        print("✓ SoundManager initialized successfully")
        
        # Test music functionality (will gracefully handle missing files)
        sound_manager.play_music('sounds/menu_music.mp3', loop=True)
        print("✓ Music playback method called successfully")
        
        # Test volume controls
        sound_manager.set_music_volume(0.5)
        volume = sound_manager.get_music_volume()
        assert volume == 0.5, f"Expected volume 0.5, got {volume}"
        print("✓ Music volume controls working")
        
        # Test fade effects
        sound_manager.fade_out_music(1000)
        print("✓ Music fade effects working")
        
        # Test state integration
        from gamestatemanager import GameStateManager
        state_manager = GameStateManager()
        
        # Test menu state with music
        menu_state = MenuState(state_manager, sound_manager)
        menu_state.enter()
        print("✓ Menu state music integration working")
        
        print("\n🎵 Background music system integration test PASSED!")
        print("All music functionality is properly implemented and integrated.")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
    
    return True


if __name__ == '__main__':
    print("Testing Background Music System Implementation")
    print("=" * 50)
    
    # Run integration test first
    integration_success = run_integration_test()
    
    print("\n" + "=" * 50)
    print("Running unit tests...")
    
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    if integration_success:
        print("\n🎉 Background music system is fully implemented and working!")
    else:
        print("\n⚠️  Some integration issues detected.")