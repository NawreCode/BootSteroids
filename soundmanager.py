import pygame
import os
from typing import Dict, Optional


class SoundManager:
    """
    Manages all audio functionality for the game including sound effects and background music.
    Handles pygame.mixer initialization gracefully and provides error handling for missing files.
    """
    
    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = 0.7
        self.sound_volume = 0.8
        self.mixer_initialized = False
        self.current_music = None
        
        # Initialize pygame mixer
        self._initialize_mixer()
        
        # Load default sounds if mixer is available
        if self.mixer_initialized:
            self._load_default_sounds()
    
    def _initialize_mixer(self) -> None:
        """Initialize pygame mixer with error handling."""
        try:
            # Initialize mixer with reasonable settings
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self.mixer_initialized = True
            print("Sound system initialized successfully")
        except pygame.error as e:
            print(f"Warning: Could not initialize sound system: {e}")
            print("Game will continue without audio")
            self.mixer_initialized = False
    
    def _load_default_sounds(self) -> None:
        """Load default sound effects with error handling."""
        # Define default sound files and their keys
        sound_files = {
            'shoot': 'sounds/shoot.wav',
            'explosion_large': 'sounds/explosion_large.wav',
            'explosion_medium': 'sounds/explosion_medium.wav',
            'explosion_small': 'sounds/explosion_small.wav',
            'player_death': 'sounds/player_death.wav',
            'extra_life': 'sounds/extra_life.wav',
            'menu_select': 'sounds/menu_select.wav',
            'menu_navigate': 'sounds/menu_navigate.wav',
            'pause': 'sounds/pause.wav',
            'unpause': 'sounds/unpause.wav'
        }
        
        for sound_key, file_path in sound_files.items():
            self.load_sound(sound_key, file_path)
    
    def load_sound(self, sound_key: str, file_path: str) -> bool:
        """
        Load a sound file and associate it with a key.
        
        Args:
            sound_key: Unique identifier for the sound
            file_path: Path to the sound file
            
        Returns:
            True if sound was loaded successfully, False otherwise
        """
        if not self.mixer_initialized:
            return False
            
        try:
            if os.path.exists(file_path):
                sound = pygame.mixer.Sound(file_path)
                sound.set_volume(self.sound_volume)
                self.sounds[sound_key] = sound
                print(f"Loaded sound: {sound_key} from {file_path}")
                return True
            else:
                print(f"Warning: Sound file not found: {file_path}")
                return False
        except pygame.error as e:
            print(f"Warning: Could not load sound {file_path}: {e}")
            return False
    
    def play_sound(self, sound_key: str) -> None:
        """
        Play a sound effect by its key.
        
        Args:
            sound_key: The key of the sound to play
        """
        if not self.mixer_initialized:
            return
            
        if sound_key in self.sounds:
            try:
                self.sounds[sound_key].play()
            except pygame.error as e:
                print(f"Warning: Could not play sound {sound_key}: {e}")
        else:
            print(f"Warning: Sound '{sound_key}' not found")
    
    def play_music(self, music_file: str, loop: bool = True) -> bool:
        """
        Play background music.
        
        Args:
            music_file: Path to the music file
            loop: Whether to loop the music (-1 for infinite loop, 0 for no loop)
            
        Returns:
            True if music started successfully, False otherwise
        """
        if not self.mixer_initialized:
            return False
            
        try:
            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops)
                self.current_music = music_file
                print(f"Playing music: {music_file}")
                return True
            else:
                print(f"Warning: Music file not found: {music_file}")
                return False
        except pygame.error as e:
            print(f"Warning: Could not play music {music_file}: {e}")
            return False
    
    def stop_music(self) -> None:
        """Stop the currently playing background music."""
        if not self.mixer_initialized:
            return
            
        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except pygame.error as e:
            print(f"Warning: Could not stop music: {e}")
    
    def pause_music(self) -> None:
        """Pause the currently playing background music."""
        if not self.mixer_initialized:
            return
            
        try:
            pygame.mixer.music.pause()
        except pygame.error as e:
            print(f"Warning: Could not pause music: {e}")
    
    def unpause_music(self) -> None:
        """Resume the paused background music."""
        if not self.mixer_initialized:
            return
            
        try:
            pygame.mixer.music.unpause()
        except pygame.error as e:
            print(f"Warning: Could not unpause music: {e}")
    
    def set_sound_volume(self, volume: float) -> None:
        """
        Set the volume for sound effects.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        
        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume: float) -> None:
        """
        Set the volume for background music.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        
        if self.mixer_initialized:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except pygame.error as e:
                print(f"Warning: Could not set music volume: {e}")
    
    def get_sound_volume(self) -> float:
        """Get the current sound effects volume."""
        return self.sound_volume
    
    def get_music_volume(self) -> float:
        """Get the current music volume."""
        return self.music_volume
    
    def is_music_playing(self) -> bool:
        """Check if background music is currently playing."""
        if not self.mixer_initialized:
            return False
            
        try:
            return pygame.mixer.music.get_busy()
        except pygame.error:
            return False
    
    def fade_out_music(self, fade_time_ms: int = 1000) -> None:
        """
        Fade out the current background music.
        
        Args:
            fade_time_ms: Time in milliseconds for the fade out effect
        """
        if not self.mixer_initialized:
            return
            
        try:
            pygame.mixer.music.fadeout(fade_time_ms)
            self.current_music = None
        except pygame.error as e:
            print(f"Warning: Could not fade out music: {e}")
    
    def fade_in_music(self, music_file: str, fade_time_ms: int = 1000, loop: bool = True) -> bool:
        """
        Fade in background music.
        
        Args:
            music_file: Path to the music file
            fade_time_ms: Time in milliseconds for the fade in effect
            loop: Whether to loop the music
            
        Returns:
            True if music started successfully, False otherwise
        """
        if not self.mixer_initialized:
            return False
            
        try:
            if os.path.exists(music_file):
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.0)  # Start at volume 0
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops, fade_ms=fade_time_ms)
                
                # Gradually increase volume to target level
                target_volume = self.music_volume
                pygame.mixer.music.set_volume(target_volume)
                
                self.current_music = music_file
                print(f"Fading in music: {music_file}")
                return True
            else:
                print(f"Warning: Music file not found: {music_file}")
                return False
        except pygame.error as e:
            print(f"Warning: Could not fade in music {music_file}: {e}")
            return False
    
    def get_current_music(self) -> Optional[str]:
        """Get the currently playing music file path."""
        return self.current_music
    
    def crossfade_music(self, new_music_file: str, fade_time_ms: int = 2000, loop: bool = True) -> bool:
        """
        Crossfade from current music to new music.
        
        Args:
            new_music_file: Path to the new music file
            fade_time_ms: Time in milliseconds for the crossfade effect
            loop: Whether to loop the new music
            
        Returns:
            True if crossfade started successfully, False otherwise
        """
        if not self.mixer_initialized:
            return False
        
        # If no music is currently playing, just fade in the new music
        if not self.is_music_playing():
            return self.fade_in_music(new_music_file, fade_time_ms, loop)
        
        # Fade out current music
        self.fade_out_music(fade_time_ms)
        
        # Schedule the new music to start after fade out completes
        # Note: In a real implementation, you'd want to use threading or a timer
        # For now, we'll just start the new music immediately
        pygame.time.wait(fade_time_ms + 100)  # Wait for fade out to complete
        return self.fade_in_music(new_music_file, fade_time_ms, loop)
    
    def cleanup(self) -> None:
        """Clean up sound resources."""
        if self.mixer_initialized:
            try:
                pygame.mixer.music.stop()
                for sound in self.sounds.values():
                    sound.stop()
                self.sounds.clear()
                pygame.mixer.quit()
                print("Sound system cleaned up")
            except pygame.error as e:
                print(f"Warning: Error during sound cleanup: {e}")