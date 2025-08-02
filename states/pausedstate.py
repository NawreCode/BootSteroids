"""
PausedState class for the pause overlay.
"""
import pygame
from states.gamestate import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PausedState(GameState):
    """Pause overlay state with resume and quit options."""
    
    def __init__(self, state_manager, playing_state, sound_manager=None):
        """Initialize the paused state."""
        super().__init__(state_manager)
        self.playing_state = playing_state  # Reference to the playing state to resume
        self.sound_manager = sound_manager or (playing_state.sound_manager if hasattr(playing_state, 'sound_manager') else None)
        self.font = None
        self.title_font = None
        self.selected_option = 0
        self.menu_options = ["Resume", "Quit to Menu"]
    
    def enter(self):
        """Called when entering the paused state."""
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        
        # Pause the background music
        if self.sound_manager:
            self.sound_manager.pause_music()
        
        print("Entered Paused State")
    
    def exit(self):
        """Called when leaving the paused state."""
        print("Exited Paused State")
    
    def update(self, dt):
        """Update pause menu logic."""
        pass
    
    def draw(self, screen):
        """Draw the pause overlay to the screen."""
        # First draw the playing state in the background (frozen)
        self.playing_state.draw(screen)
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill("black")
        screen.blit(overlay, (0, 0))
        
        # Draw pause title
        title_text = self.title_font.render("PAUSED", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.menu_options):
            color = "yellow" if i == self.selected_option else "white"
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
            screen.blit(option_text, option_rect)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to select",
            "ESC to resume"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = instruction_font.render(instruction, True, "gray")
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100 + i * 25))
            screen.blit(instruction_text, instruction_rect)
    
    def handle_event(self, event):
        """Handle pause menu events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.sound_manager:
                    self.sound_manager.play_sound('menu_navigate')
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                if self.sound_manager:
                    self.sound_manager.play_sound('menu_navigate')
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.sound_manager:
                    self.sound_manager.play_sound('menu_select')
                if self.selected_option == 0:  # Resume
                    if self.sound_manager:
                        self.sound_manager.play_sound('unpause')
                        self.sound_manager.unpause_music()
                    # Return to the playing state
                    self.state_manager.change_state(self.playing_state)
                elif self.selected_option == 1:  # Quit to Menu
                    # Clean up playing state and go to menu
                    self.playing_state.exit()
                    from states.menustate import MenuState
                    self.state_manager.change_state(MenuState(self.state_manager, self.sound_manager))
            elif event.key == pygame.K_ESCAPE:
                if self.sound_manager:
                    self.sound_manager.play_sound('unpause')
                    self.sound_manager.unpause_music()
                # Resume game when ESC is pressed
                self.state_manager.change_state(self.playing_state)