from typing import override

import pygame

from .game_state import GameState
from src.objects.game_object import GameObject


class PlayGameState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)
        self.entities: list = []

        my_object = GameObject()
        self.entities.append(my_object)

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
