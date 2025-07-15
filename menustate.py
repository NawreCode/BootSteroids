"""
MenuState class for the main menu.
"""
import pygame
from gamestate import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuState(GameState):
    """Main menu state with simple menu rendering."""
    
    def __init__(self, state_manager):
        """Initialize the menu state."""
        super().__init__(state_manager)
        self.font = None
        self.title_font = None
        self.selected_option = 0
        self.menu_options = ["Start Game", "Quit"]
    
    def enter(self):
        """Called when entering the menu state."""
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        print("Entered Menu State")
    
    def exit(self):
        """Called when leaving the menu state."""
        print("Exited Menu State")
    
    def update(self, dt):
        """Update menu logic."""
        pass
    
    def draw(self, screen):
        """Draw the menu to the screen."""
        screen.fill("black")
        
        # Draw title
        title_text = self.title_font.render("ASTEROIDS", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
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
            "ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = instruction_font.render(instruction, True, "gray")
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100 + i * 25))
            screen.blit(instruction_text, instruction_rect)
    
    def handle_event(self, event):
        """Handle menu events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Start Game
                    # Import here to avoid circular imports
                    from playingstate import PlayingState
                    self.state_manager.change_state(PlayingState(self.state_manager))
                elif self.selected_option == 1:  # Quit
                    pygame.quit()
                    exit()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()