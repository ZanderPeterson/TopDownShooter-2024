from math import pi
from typing import Any, Dict, List, override, Tuple, TypeAlias

import pygame

from .game_state import GameState
from src.objects import GameObject, PlayerObject, BulletObject, WallObject
from src.utils import find_vector_between, move_by_vector, orbit_around_circle

Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class PlayGameState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)
        self.entities: Dict[str, GameObject] = {}
        self.bullets: List[BulletObject] = []

        self.track_keys: Dict[int, bool] = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
        }
        self.track_clicks: Dict[int, bool] = {
            1: False, #Left Click
            2: False, #Middle Click
            3: False, #Right Click
        }
        self.constants: Dict[str, Any] = {
            "forward_speed": 3,
            "backward_speed": 3,
            "sideways_speed": 3,
            "bullet_speed": 5,
            "fire_rate": 60,
        }
        self.game_variables: Dict[str, Any] = {
            "time_before_next_shot": 0,
        }

        self.entities["player"] = PlayerObject(start_pos=(100-16, 100-16),
                                               forward_speed=self.constants["forward_speed"],
                                               backward_speed=self.constants["backward_speed"],
                                               sideways_speed=self.constants["sideways_speed"],)

    @override
    def enter(self) -> None:
        print("Entering the Play Game state.")

        for key in self.track_keys.keys():
            self.track_keys[key] = False

        for click in self.track_clicks.keys():
            self.track_clicks[click] = False

    @override
    def exit(self) -> None:
        print("Exiting the Play Game state.")

    @override
    def update(self) -> None:
        #Gets position of the mouse, and finds the Vector from the centre of the player to it.
        mouse_pos = pygame.mouse.get_pos()
        vector_to_cursor: Vector = find_vector_between(self.entities["player"].centre, mouse_pos)

        #Rotates the player to look at the mouse.
        self.entities["player"].set_rotation(vector_to_cursor[1])

        #Code that backs the player away from the cursor if the cursor is too close to the player's centre.
        if vector_to_cursor[0] < 10:
            self.entities["player"].move_backward(vector_to_cursor, move_by=10-vector_to_cursor[0])

        #A & D Movement Code
        if not (self.track_keys[pygame.K_a] and self.track_keys[pygame.K_d]):
            if self.track_keys[pygame.K_a]:
                self.entities["player"].move_leftward(vector_to_cursor)
            elif self.track_keys[pygame.K_d]:
                self.entities["player"].move_rightward(vector_to_cursor)

        #W & S Movement Code
        if not (self.track_keys[pygame.K_w] and self.track_keys[pygame.K_s]):
            if self.track_keys[pygame.K_w]:
                self.entities["player"].move_forward(vector_to_cursor)
            elif self.track_keys[pygame.K_s]:
                self.entities["player"].move_backward(vector_to_cursor)

        #Countdown the time before next shot.
        if self.game_variables["time_before_next_shot"] > 0:
            self.game_variables["time_before_next_shot"] -= 1

        #Spawn Projectiles Code
        if self.track_clicks[1]:
            if self.game_variables["time_before_next_shot"] <= 0:
                new_bullet: BulletObject = BulletObject(rotation=self.entities["player"].rotation,
                                                        speed=self.constants["bullet_speed"])
                new_bullet.set_position_by_centre(self.entities["player"].centre)
                self.bullets.append(new_bullet)
                self.game_variables["time_before_next_shot"] = self.constants["fire_rate"]

        #Updates all bullet positions.
        for bullet in self.bullets:
            bullet.update()

    @override
    def render(self, window) -> None:
        #Renders the background.
        window.fill((0, 0, 0))

        #Loops through all the entities and renders them to the screen.
        for entity in self.entities.values():
            window.blit(entity.render_image(), entity.get_image_position())

        # Loops through all the bullets and renders them to the screen.
        for bullet in self.bullets:
            window.blit(bullet.render_image(), bullet.get_image_position())

    @override
    def handle_event(self, event) -> None | str:
        #Record down keypresses.
        if event.type == pygame.KEYDOWN and event.key in self.track_keys:
            self.track_keys[event.key] = True
        elif event.type == pygame.KEYUP and event.key in self.track_keys:
            self.track_keys[event.key] = False

        #Record down mouse clicks.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in self.track_clicks:
            self.track_clicks[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button in self.track_clicks:
            self.track_clicks[event.button] = False
        return None
