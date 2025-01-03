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
            image = "missing_texture_32x32.png"
        image = os.path.join(os.path.join("assets", "images"), image)

        self.image: str = image #A directory to the image associated with this object.
        self.loaded_image = pygame.image.load(self.image).convert_alpha()

        self.img_offset: coords = (0, 0)  # How far to offset the sprite's image to account for rotation.
        self.img_size: Tuple[float, float] = self.loaded_image.get_size()
        self.centre: coords = (self.position[0] + self.img_size[0]/2,
                               self.position[1] + self.img_size[1]/2)

    def render_image(self):
        """Returns a rendered image that can be blitted to the screen."""
        to_return = self.loaded_image

        #Scales the image
        #NEED TO IMPLEMENT
        #...eventually. If it is needed. However, I currently fail to believe that image scaling is a requirement.

        #Rotates the image
        to_return = pygame.transform.rotate(to_return, degrees(self.rotation))
        rotated_img_size: coords = to_return.get_size()
        self.img_offset = (self.img_size[0]/2 - rotated_img_size[0]/2,
                           self.img_size[1]/2 - rotated_img_size[1]/2)
        self.centre = (self.get_image_position()[0] + rotated_img_size[0]/2,
                       self.get_image_position()[1] + rotated_img_size[1]/2)
        return to_return

    def get_image_position(self):
        """Returns the position that the image needs to be drawn at."""
        return (self.position[0] + self.img_offset[0],
                self.position[1] + self.img_offset[1])

    def get_centre_position(self):
        """Returns the position of the centre of the sprite."""
        return (self.position[0] + self.img_size[0]/2,
                self.position[1] + self.img_size[1]/2)

    def set_position(self, position: coords = (0, 0)) -> None:
        """Sets the Object's position."""
        self.position = (float(position[0]), float(position[1]))

    def set_position_by_centre(self, position: coords = (0, 0)) -> coords:
        """Sets the Object's Position, but sets the centre of the sprite as opposed
        to the top left corner of the sprite. Returns new position."""
        self.position = (float(position[0] - self.img_size[0]/2),
                         float(position[1] - self.img_size[1]/2))
        return self.position

    def move_by_amount(self, position: coords) -> coords:
        """Moves the Object's position by an amount. Returns new position."""
        self.position = (self.position[0] + position[0],
                         self.position[1] + position[1])
        return self.position

    def set_rotation(self, rotation: float | None = None):
        """Sets the rotation of the sprite."""
        self.rotation = float(rotation)

    def rotate_by(self, rotate_by: float) -> float:
        """Rotates the object counterclockwise. Returns new rotation."""
        self.set_rotation(self.rotation + rotate_by)
        return self.rotation
