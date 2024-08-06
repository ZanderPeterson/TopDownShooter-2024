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
        self.tag: str | None = tag #When dealing with collisions, this should help.
        self.position: coords = start_pos #The object's position.
        self.rotation: float = rotation #The object's rotation. Rotation measured in Radians (NOT DEGREES)
        self.image: str = image #A directory to the image associated with this object.

    def set_position(self, position: coords = (0, 0)) -> None:
        """Sets the Object's position."""
        self.position = (float(position[0]), float(position[1]))

    def move_by_amount(self, position: coords) -> coords:
        """Moves the Object's position by an amount. Returns new position."""
        self.position = (self.position[0] + position[0],
                         self.position[1] + position[1])
        return self.position

    def rotate_left_by(self, rotate_by: float) -> float:
        """Rotates the object left. Returns new rotation."""
        self.rotation = self.rotate - rotate_by
        return self.rotation

    def rotate_right_by(self, rotate_by: float) -> float:
        """Rotates the object right. Returns new rotation."""
        self.rotation = self.rotate + rotate_by
        return self.rotation
