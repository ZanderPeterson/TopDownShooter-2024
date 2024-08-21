#This file is intended for running the game loop

import sys
import os

import pygame

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.game import Game
from src.settings import Settings

def main() -> None:
    width: int = Settings.WINDOW_WIDTH
    height: int = Settings.WINDOW_HEIGHT
    FPS: int = Settings.FPS
    
    pygame.init()
    window = pygame.display.set_mode((width, height))
    game = Game(window)
    pygame.display.set_caption(Settings.WINDOW_CAPTION)
    clock = pygame.time.Clock()
    running: bool = True

    #Main Gameloop
    while running:
        #Keeps the FPS capped to a value.
        clock.tick(FPS)

        #Handles the events, such as keypresses.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        #Updates the current state.
        game.update()

        #Renders everything and puts it onto the window.
        game.render()
        pygame.display.flip()

    #Exits the window.
    pygame.quit()

if __name__ == "__main__":
    main()
