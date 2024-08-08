# This file is intended for running the game loop.
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

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        game.update()
        game.render()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
