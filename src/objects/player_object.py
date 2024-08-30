from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import move_by_vector, orbit_around_circle, reverse_vector

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class PlayerObject(GameObject):
    """A Subclass of GameObject which is intended to be used as the player."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 image: str | None = None) -> None:
        super().__init__(tag="player", start_pos=start_pos, rotation=rotation, image=image)
        self.forward_speed = 3
        self.backward_speed = 3
        self.sideways_speed = 100

    def move_forward(self, vector_to_cursor: Vector, move_by: float | None = None) -> coords:
        """
        Moves the player forward (towards the cursor).
        Returns the new player's position.
        """
        if not move_by:
            move_by = self.forward_speed

        change_pos_by: coords = move_by_vector((0, 0), (move_by, vector_to_cursor[1]))
        self.move_by_amount(change_pos_by)
        return self.position

    def move_backward(self, vector_to_cursor: Vector, move_by: float | None = None) -> coords:
        """
        Moves the player backward (towards the cursor).
        Returns the new player's position.
        """
        if not move_by:
            move_by = self.backward_speed

        self.move_forward(reverse_vector(vector_to_cursor), move_by)
        return self.position

    def move_rightward(self, vector_to_cursor: Vector, move_by: float | None = None) -> coords:
        """
        Moves the player rightward (towards the cursor).
        Returns the new player's position.
        """
        if not move_by:
            move_by = self.sideways_speed

        new_position: coords = orbit_around_circle(self.centre, vector_to_cursor, move_by)
        self.set_position_by_centre(new_position)

        return self.position
