"""
GameStateManager class to handle state transitions and delegation.
"""
import pygame


class GameStateManager:
    """Manages game states and handles transitions between them."""
    
    def __init__(self):
        """Initialize the game state manager."""
        self.current_state = None
        self.next_state = None
    
    def change_state(self, new_state):
        """Queue a state change to occur at the next update."""
        self.next_state = new_state
    
    def update(self, dt):
        """Update the current state and handle state transitions."""
        # Handle state transitions
        if self.next_state is not None:
            if self.current_state is not None:
                self.current_state.exit()
            
            self.current_state = self.next_state
            self.next_state = None
            self.current_state.enter()
        
        # Update current state
        if self.current_state is not None:
            self.current_state.update(dt)
    
    def draw(self, screen):
        """Draw the current state."""
        if self.current_state is not None:
            self.current_state.draw(screen)
    
    def handle_event(self, event):
        """Handle events by delegating to the current state."""
        if self.current_state is not None:
            self.current_state.handle_event(event)