from typing import Tuple, TypeAlias

import pygame

coords: TypeAlias = Tuple[float, float]


class GameObject():
    """A class intended to be inherited from to handle object related functions."""

    def __init__(self,
                 tag: str | None = None,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 image: str = "assets/images/missing_texture_32x32") -> None:
        self.tag: str | None = tag
        self.position: coords = start_pos
        self.rotation: rotation
        self.image: str = image

    def set_position(self, position: coords = (0, 0)) -> None:
        self.position = (float(position[0]), float(position[1]))

    def move_by_amount(self, position: coords) -> coords:
        self.position = (self.position[0] + position[0],
                         self.position[1] + position[1])
        return self.position
