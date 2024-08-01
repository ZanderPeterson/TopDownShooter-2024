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
        # Main Menu rendering to be done here.
