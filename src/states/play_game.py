from math import pi
from typing import Dict, List, Tuple, override, TypeAlias

import pygame

from .game_state import GameState
from src.objects.game_object import GameObject
from src.objects.player_object import PlayerObject
from src.utils import find_vector_between, move_by_vector

Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


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

        self.entities["player"] = PlayerObject(start_pos=(300, 300))

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
        FORWARD_SPEED = 2
        mouse_pos = pygame.mouse.get_pos()
        vector_to_cursor: Vector = find_vector_between(self.entities["player"].centre, mouse_pos)
        self.entities["player"].set_rotation(vector_to_cursor[1])
        move_by = move_by_vector((0, 0),
                                 (min(vector_to_cursor[0], FORWARD_SPEED), vector_to_cursor[1]))
        self.entities["player"].move_by_amount(move_by)

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
