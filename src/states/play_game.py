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

        self.entities["player"] = PlayerObject(start_pos=(100-16, 100-16))

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
        #Define some variables... maybe not the best way to do it.
        FORWARD_SPEED: float = 2
        BACKWARD_SPEED: float = 1.5

        #Gets position of the mouse, and finds the Vector from the centre of the player to it.
        mouse_pos = pygame.mouse.get_pos()
        vector_to_cursor: Vector = find_vector_between(self.entities["player"].centre, mouse_pos)

        #Rotates the player to look at the mouse.
        self.entities["player"].set_rotation(vector_to_cursor[1])
        #print(self.entities["player"].centre)

        #W & S Movement Code
        if not (self.track_keys[pygame.K_w] and self.track_keys[pygame.K_s]):
            forward_back_speed: float = 0
            if self.track_keys[pygame.K_w]:
                forward_back_speed = FORWARD_SPEED
            elif self.track_keys[pygame.K_s]:
                forward_back_speed = -BACKWARD_SPEED
            move_forward_by: Vector = move_by_vector((0, 0),
                                                     (forward_back_speed, vector_to_cursor[1]))
            self.entities["player"].move_by_amount(move_forward_by)

    @override
    def render(self, window) -> None:
        #Renders the background.
        window.fill((0, 0, 0))

        #Loops through all the entities and renders them to the screen.
        for entity in self.entities.values():
            #print(entity.get_image_position())
            window.blit(entity.render_image(), entity.get_image_position())

    @override
    def handle_event(self, event) -> None | str:
        #Record down keypresses.
        if event.type == pygame.KEYDOWN and event.key in self.track_keys:
            self.track_keys[event.key] = True
        elif event.type == pygame.KEYUP and event.key in self.track_keys:
            self.track_keys[event.key] = False
        return None
