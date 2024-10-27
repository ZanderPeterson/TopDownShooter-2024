from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import move_by_vector, orbit_around_circle, reverse_vector

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class EnemyObject(GameObject):
    """A Subclass of GameObject which is intended to be used as the enemy."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 start_hp: int = 0,
                 cooldown: int = 0,
                 accuracy: float = 0,
                 image: str | None = None) -> None:
        super().__init__(tag="enemy", start_pos=start_pos, rotation=rotation, image=image)
        self.health = start_hp
        self.cooldown = cooldown
        self.accuracy = accuracy

