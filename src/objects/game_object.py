import os
from math import degrees
from typing import Tuple, TypeAlias

import pygame

coords: TypeAlias = Tuple[float, float]


class GameObject():
    """A class intended to be inherited from to handle object related functions."""

    def __init__(self,
                 tag: str | None = None,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 image: str | None = None) -> None:
        self.tag: str | None = tag #When dealing with collisions, this should help.
        self.position: coords = start_pos #The object's position.
        self.rotation: float = rotation #The object's rotation. Rotation measured in Radians (NOT DEGREES)

        if not image:
            image = os.path.join(os.path.join("assets", "images"), "missing_texture_32x32.png")
        self.image: str = image #A directory to the image associated with this object.
        self.loaded_image = pygame.image.load(self.image).convert_alpha()

    def render_image(self):
        """Returns a rendered image that can be blitted to the screen."""
        to_return = self.loaded_image

        #Scales the image
        #NEED TO IMPLEMENT
        #...eventually. If it is needed. However, I currently fail to believe that image scaling is a requirement.

        #Rotates the image
        to_return = pygame.transform.rotate(to_return, degrees(self.rotation))
        return to_return

    def set_position(self, position: coords = (0, 0)) -> None:
        """Sets the Object's position."""
        self.position = (float(position[0]), float(position[1]))

    def move_by_amount(self, position: coords) -> coords:
        """Moves the Object's position by an amount. Returns new position."""
        self.position = (self.position[0] + position[0],
                         self.position[1] + position[1])
        return self.position

    def rotate_by(self, rotate_by: float) -> float:
        """Rotates the object counterclockwise. Returns new rotation."""
        self.rotation = self.rotation + rotate_by
        return self.rotation
