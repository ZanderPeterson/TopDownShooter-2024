from typing import Dict, override

import pygame

from .game_state import GameState
from src.objects.game_object import GameObject


class PlayGameState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)
        self.entities: Dict[str, GameObject] = {}

        self.entities["my_object"] = GameObject()

    @override
    def enter(self) -> None:
        print("Entering the Play Game state.")

    @override
    def exit(self) -> None:
        print("Exiting the Play Game state.")

    @override
    def update(self) -> None:
        self.entities["my_object"].set_position()

    @override
    def render(self, window) -> None:
        window.fill((0, 0, 0))

        #Loops through all the entities and renders them to the screen.
        for entity in self.entities.values():
            window.blit(entity.render_image(), entity.position)
