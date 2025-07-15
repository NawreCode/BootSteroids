"""
Base GameState abstract class for managing different game states.
"""
from abc import ABC, abstractmethod
import pygame


class GameState(ABC):
    """Abstract base class for all game states."""
    
    def __init__(self, state_manager):
        """Initialize the game state with a reference to the state manager."""
        self.state_manager = state_manager
    
    @abstractmethod
    def enter(self):
        """Called when entering this state."""
        pass
    
    @abstractmethod
    def exit(self):
        """Called when leaving this state."""
        pass
    
    @abstractmethod
    def update(self, dt):
        """Update the state logic."""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """Draw the state to the screen."""
        pass
    
    @abstractmethod
    def handle_event(self, event):
        """Handle pygame events."""
        pass