# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from gamestatemanager import GameStateManager
from menustate import MenuState


def main():
    print("Starting Asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    clock = pygame.time.Clock()
    dt = 0

    # Initialize game state manager and start with menu
    state_manager = GameStateManager()
    initial_state = MenuState(state_manager)
    state_manager.change_state(initial_state)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            state_manager.handle_event(event)

        state_manager.update(dt)
        state_manager.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()
