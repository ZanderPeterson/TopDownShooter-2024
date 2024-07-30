# This file is intended for running the game loop.
# This is a test.

import pygame

import src.settings as settings


def main() -> None:
    width: int = settings.WINDOW_WIDTH
    height: int = settings.WINDOW_HEIGHT
    FPS: int = settings.FPS
    
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('L1DIT Basic Shooter')
    clock = pygame.time.Clock()
    running: bool = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
