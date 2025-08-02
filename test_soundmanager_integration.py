#!/usr/bin/env python3
"""
Integration test for SoundManager to verify it works with actual pygame initialization.
This test will run the SoundManager in a real environment.
"""

import pygame
from soundmanager import SoundManager


def test_soundmanager_integration():
    """Test SoundManager with actual pygame initialization."""
    print("Testing SoundManager integration...")
    
    # Initialize pygame (required for mixer)
    pygame.init()
    
    try:
        # Create SoundManager instance
        sound_manager = SoundManager()
        
        print(f"Mixer initialized: {sound_manager.mixer_initialized}")
        print(f"Sound volume: {sound_manager.get_sound_volume()}")
        print(f"Music volume: {sound_manager.get_music_volume()}")
        
        # Test volume controls
        print("\nTesting volume controls...")
        sound_manager.set_sound_volume(0.5)
        sound_manager.set_music_volume(0.6)
        print(f"New sound volume: {sound_manager.get_sound_volume()}")
        print(f"New music volume: {sound_manager.get_music_volume()}")
        
        # Test loading non-existent sound (should handle gracefully)
        print("\nTesting non-existent sound loading...")
        result = sound_manager.load_sound('test_sound', 'nonexistent.wav')
        print(f"Load result for non-existent file: {result}")
        
        # Test playing non-existent sound (should handle gracefully)
        print("\nTesting non-existent sound playback...")
        sound_manager.play_sound('nonexistent_sound')
        print("Non-existent sound playback handled gracefully")
        
        # Test music operations (should handle gracefully with non-existent file)
        print("\nTesting music operations...")
        music_result = sound_manager.play_music('nonexistent_music.mp3')
        print(f"Music play result for non-existent file: {music_result}")
        
        print(f"Is music playing: {sound_manager.is_music_playing()}")
        
        # Test cleanup
        print("\nTesting cleanup...")
        sound_manager.cleanup()
        print("Cleanup completed successfully")
        
        print("\n✅ SoundManager integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        raise
    finally:
        pygame.quit()


if __name__ == '__main__':
    test_soundmanager_integration()