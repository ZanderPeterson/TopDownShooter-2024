from typing import override

import pygame

from .game_state import GameState


class PlayGameState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)

        # Initialise all the game entities here

    @override
    def enter(self) -> None:
        print("Entering the Play Game state.")

    @override
    def exit(self) -> None:
        print("Exiting the Play Game state.")

    @override
    def render(self, window) -> None:
        window.fill((0, 0, 0))
        # Game Entity rendering to be done here.

    @override
    def handle_event(self, event) -> None | str:
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            return "PlayGame"
        return None
