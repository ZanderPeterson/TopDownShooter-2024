# This file is intended for running the game loop.

import pygame

import src.settings as settings

from .game import Game

def main() -> None:
    width: int = settings.WINDOW_WIDTH
    height: int = settings.WINDOW_HEIGHT
    FPS: int = settings.FPS
    
    pygame.init()
    window = pygame.display.set_mode((width, height))
    game = Game(window)
    pygame.display.set_caption(settings.WINDOW_CAPTION)
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

    pygame.quit()

if __name__ == "__main__":
    main()
