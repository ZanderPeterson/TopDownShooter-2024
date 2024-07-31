from typing import override

import pygame

from .game_state import GameState

class MainMenuState(GameState):
    """A Subclass of GameState intended to handle the Main Menu."""

    def __init__(self, game) -> None:
        super().__init__(game)

    @override
    def enter(self) -> None:
        print("Entering the Main Menu state.")

    @override
    def exit(self) -> None:
        print("Exiting the Main Menu state.")

    @override
    def render(self, window) -> None:
        window.fill((0, 0, 0))
