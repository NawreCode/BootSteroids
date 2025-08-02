import unittest
from unittest.mock import patch, MagicMock
import pygame
from soundmanager import SoundManager


class TestSoundManager(unittest.TestCase):
    """Test cases for the SoundManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock pygame.mixer to avoid actual audio initialization during tests
        self.mixer_patcher = patch('pygame.mixer')
        self.mock_mixer = self.mixer_patcher.start()
        
        # Mock os.path.exists to control file existence checks
        self.exists_patcher = patch('os.path.exists')
        self.mock_exists = self.exists_patcher.start()
        
    def tearDown(self):
        """Clean up after tests."""
        self.mixer_patcher.stop()
        self.exists_patcher.stop()
    
    def test_initialization_success(self):
        """Test successful SoundManager initialization."""
        self.mock_mixer.init.return_value = None
        self.mock_exists.return_value = False  # No sound files exist
        
        sound_manager = SoundManager()
        
        self.assertTrue(sound_manager.mixer_initialized)
        self.assertEqual(sound_manager.music_volume, 0.7)
        self.assertEqual(sound_manager.sound_volume, 0.8)
        self.mock_mixer.pre_init.assert_called_once()
        self.mock_mixer.init.assert_called_once()
    
    def test_initialization_failure(self):
        """Test SoundManager initialization when pygame.mixer fails."""
        self.mock_mixer.init.side_effect = pygame.error("Mixer initialization failed")
        
        sound_manager = SoundManager()
        
        self.assertFalse(sound_manager.mixer_initialized)
    
    def test_load_sound_success(self):
        """Test successful sound loading."""
        self.mock_mixer.init.return_value = None
        self.mock_exists.return_value = True
        mock_sound = MagicMock()
        self.mock_mixer.Sound.return_value = mock_sound
        
        sound_manager = SoundManager()
        result = sound_manager.load_sound('test_sound', 'test.wav')
        
        self.assertTrue(result)
        self.assertIn('test_sound', sound_manager.sounds)
        mock_sound.set_volume.assert_called_with(0.8)
    
    def test_load_sound_file_not_found(self):
        """Test sound loading when file doesn't exist."""
        self.mock_mixer.init.return_value = None
        self.mock_exists.return_value = False
        
        sound_manager = SoundManager()
        result = sound_manager.load_sound('test_sound', 'nonexistent.wav')
        
        self.assertFalse(result)
        self.assertNotIn('test_sound', sound_manager.sounds)
    
    def test_play_sound_success(self):
        """Test successful sound playback."""
        self.mock_mixer.init.return_value = None
        self.mock_exists.return_value = True
        mock_sound = MagicMock()
        self.mock_mixer.Sound.return_value = mock_sound
        
        sound_manager = SoundManager()
        sound_manager.load_sound('test_sound', 'test.wav')
        sound_manager.play_sound('test_sound')
        
        mock_sound.play.assert_called_once()
    
    def test_play_sound_not_found(self):
        """Test playing a sound that doesn't exist."""
        self.mock_mixer.init.return_value = None
        
        sound_manager = SoundManager()
        # This should not raise an exception
        sound_manager.play_sound('nonexistent_sound')
    
    def test_play_music_success(self):
        """Test successful music playback."""
        self.mock_mixer.init.return_value = None
        self.mock_exists.return_value = True
        
        sound_manager = SoundManager()
        result = sound_manager.play_music('test_music.mp3', loop=True)
        
        self.assertTrue(result)
        self.mock_mixer.music.load.assert_called_with('test_music.mp3')
        self.mock_mixer.music.set_volume.assert_called_with(0.7)
        self.mock_mixer.music.play.assert_called_with(-1)
    
    def test_volume_control(self):
        """Test volume control functionality."""
        self.mock_mixer.init.return_value = None
        
        sound_manager = SoundManager()
        
        # Test sound volume
        sound_manager.set_sound_volume(0.5)
        self.assertEqual(sound_manager.get_sound_volume(), 0.5)
        
        # Test music volume
        sound_manager.set_music_volume(0.3)
        self.assertEqual(sound_manager.get_music_volume(), 0.3)
        self.mock_mixer.music.set_volume.assert_called_with(0.3)
    
    def test_volume_clamping(self):
        """Test that volume values are clamped to valid range."""
        self.mock_mixer.init.return_value = None
        
        sound_manager = SoundManager()
        
        # Test values above 1.0
        sound_manager.set_sound_volume(1.5)
        self.assertEqual(sound_manager.get_sound_volume(), 1.0)
        
        # Test values below 0.0
        sound_manager.set_music_volume(-0.5)
        self.assertEqual(sound_manager.get_music_volume(), 0.0)
    
    def test_mixer_not_initialized(self):
        """Test behavior when mixer is not initialized."""
        self.mock_mixer.init.side_effect = pygame.error("No audio device")
        
        sound_manager = SoundManager()
        
        # These should not raise exceptions
        self.assertFalse(sound_manager.load_sound('test', 'test.wav'))
        sound_manager.play_sound('test')
        self.assertFalse(sound_manager.play_music('test.mp3'))
        sound_manager.stop_music()
        sound_manager.pause_music()
        sound_manager.unpause_music()
        self.assertFalse(sound_manager.is_music_playing())


if __name__ == '__main__':
    unittest.main()