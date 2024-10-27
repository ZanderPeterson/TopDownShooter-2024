from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import find_vector_between

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
        self.health: int = start_hp
        self.max_cooldown: int = cooldown
        self.cooldown: int = self.max_cooldown
        self.accuracy: float = accuracy

    def update(self):
        """Updates the enemy."""
        self.max_cooldown = max(self.cooldown - 1, 0)

    def aim_in_direction(self, target_centre) -> float:
        """Takes in a target's position, and figures out where to look"""
        self.rotation = find_vector_between(self.position, target_centre)[1]
        return self.rotation

    def check_if_shot_allowed(self):
        """Checks if the cooldown is at 0"""
        return self.cooldown <= 0

