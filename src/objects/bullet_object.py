from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class BulletObject(GameObject):
    """A Subclass of GameObject which is intended to be used for projectiles."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 movement: Vector | None = None,
                 image: str | None = None) -> None:
        super().__init__(tag="bullet", start_pos=start_pos, rotation=rotation, image=image)
        if not movement:
            movement = (0, 0)
        self.movement = movement
