from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import move_by_vector

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class BulletObject(GameObject):
    """A Subclass of GameObject which is intended to be used for projectiles."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 speed: float | None = None,
                 image: str | None = None) -> None:
        super().__init__(tag="bullet", start_pos=start_pos, rotation=rotation, image=image)
        if not speed:
            speed = 0
        self.speed: float = speed

    def get_vector(self) -> Vector:
        """Returns a vector which is just the (rotation, speed)"""
        return (self.rotation, self.speed)

    def update(self) -> None:
        """Moved the bullet  by its speed and rotation."""
        self.position = move_by_vector(self.position,
                                       self.get_vector())
