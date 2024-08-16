from math import pi
from typing import Dict, List, override

import pygame

from .game_state import GameState
from src.objects.game_object import GameObject
from src.objects.player_object import PlayerObject
from src.utils import find_vector_between


class PlayGameState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)
        self.entities: Dict[str, GameObject] = {}
        self.track_keys: Dict[int, bool] = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
        }

        self.entities["my_object"] = GameObject()

    @override
    def enter(self) -> None:
        print("Entering the Play Game state.")

        for key in self.track_keys.keys():
            self.track_keys[key] = False

    @override
    def exit(self) -> None:
        print("Exiting the Play Game state.")

    @override
    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        print(find_vector_between(self.entities["my_object"].centre, mouse_pos))

    @override
    def render(self, window) -> None:
        window.fill((0, 0, 0))

        #Loops through all the entities and renders them to the screen.
        for entity in self.entities.values():
            #print(entity.get_image_position())
            window.blit(entity.render_image(), entity.get_image_position())

    def handle_event(self, event) -> None | str:
        # Record down keypresses.
        if event.type == pygame.KEYDOWN and event.key in self.track_keys:
            self.track_keys[event.key] = True
        elif event.type == pygame.KEYUP and event.key in self.track_keys:
            self.track_keys[event.key] = False
        return None
