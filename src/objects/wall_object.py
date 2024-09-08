from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import find_object_corner, move_by_vector

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction
size: TypeAlias = Tuple[float, float] #width, height


class WallObject(GameObject):
    """A Subclass of GameObject which is intended to be used for walls."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 image: str | None = None) -> None:
        super().__init__(tag="wall", start_pos=start_pos, rotation=rotation, image=image)

    @classmethod
    def right_of_wall(cls, ref_wall: WallObject, image: str | None) -> WallObject:
        """This method constructs a new WallObject with a position to the right of another wall."""
        object_corner = find_object_corner(ref_wall.position, ref_wall.centre, ref_wall.rotation)
        new_wall_position = move_by_vector(object_corner, (ref_wall.img_size[0], ref_wall.rotation))
        return cls(new_wall_position, self.rotation, image)
