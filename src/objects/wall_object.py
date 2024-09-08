from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import find_object_corner, move_by_vector, reverse_vector

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
    def relative_to_wall(cls, ref_wall: 'WallObject', new_pos_vector: Vector, image: str | None) -> 'WallObject':
        """Constructs a new WallObject with a position relative to another wall."""
        object_corner = find_object_corner(ref_wall.position, ref_wall.centre, ref_wall.rotation)
        new_wall_position = move_by_vector(object_corner, new_pos_vector)
        return cls(new_wall_position, ref_wall.rotation, image)

    @classmethod
    def right_of_wall(cls, ref_wall: 'WallObject', image: str | None) -> 'WallObject':
        """Constructs a new WallObject with a position to the right of another wall."""
        return cls.relative_to_wall(ref_wall, (ref_wall.img_size[0], ref_wall.rotation), image)

    @classmethod
    def left_of_wall(cls, ref_wall: 'WallObject', image: str | None) -> 'WallObject':
        """Constructs a new WallObject with a position to the left of another wall."""
        return cls.relative_to_wall(ref_wall, reverse_vector(ref_wall.img_size[0], ref_wall.rotation), image)

    @classmethod
    def above_wall(cls, ref_wall: 'WallObject', image: str | None) -> 'WallObject':
        """Constructs a new WallObject with a position above another wall."""
        return cls.relative_to_wall(ref_wall, (ref_wall.img_size[1], ref_wall.rotation), image)

    @classmethod
    def below_wall(cls, ref_wall: 'WallObject', image: str | None) -> 'WallObject':
        """Constructs a new WallObject with a position below another wall."""
        return cls.relative_to_wall(ref_wall, reverse_vector(ref_wall.img_size[1], ref_wall.rotation), image)
