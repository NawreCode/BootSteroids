"""
GameOverState class for the game over screen.
"""
import pygame
from gamestate import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverState(GameState):
    """Game over screen with score display and restart options."""
    
    def __init__(self, state_manager, final_score=0):
        """Initialize the game over state."""
        super().__init__(state_manager)
        self.final_score = final_score
        self.font = None
        self.title_font = None
        self.score_font = None
        self.selected_option = 0
        self.menu_options = ["Restart", "Main Menu"]
    
    def enter(self):
        """Called when entering the game over state."""
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 36)
        print("Entered Game Over State")
    
    def exit(self):
        """Called when leaving the game over state."""
        print("Exited Game Over State")
    
    def update(self, dt):
        """Update game over logic."""
        pass
    
    def draw(self, screen):
        """Draw the game over screen."""
        screen.fill("black")
        
        # Draw game over title
        title_text = self.title_font.render("GAME OVER", True, "red")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Draw final score
        score_text = self.score_font.render(f"Final Score: {self.final_score}", True, "white")
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, score_rect)
        
        # TODO: Add high score display when scoring system is implemented
        # high_score_text = self.score_font.render(f"High Score: {high_score}", True, "yellow")
        # high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 40))
        # screen.blit(high_score_text, high_score_rect)
        
        # Draw menu options
        for i, option in enumerate(self.menu_options):
            color = "yellow" if i == self.selected_option else "white"
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 + i * 60))
            screen.blit(option_text, option_rect)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to select",
            "ESC for main menu"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = instruction_font.render(instruction, True, "gray")
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100 + i * 25))
            screen.blit(instruction_text, instruction_rect)
    
    def handle_event(self, event):
        """Handle game over screen events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Restart
                    # Start a new game
                    from playingstate import PlayingState
                    self.state_manager.change_state(PlayingState(self.state_manager))
                elif self.selected_option == 1:  # Main Menu
                    # Return to main menu
                    from menustate import MenuState
                    self.state_manager.change_state(MenuState(self.state_manager))
            elif event.key == pygame.K_ESCAPE:
                # Go to main menu when ESC is pressed
                from menustate import MenuState
                self.state_manager.change_state(MenuState(self.state_manager))