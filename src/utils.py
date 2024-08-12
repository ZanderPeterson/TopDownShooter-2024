# This file is for functions I might need, such as Vector Mathematics

import math

from typing import Tuple, TypeAlias

coords: TypeAlias = Tuple[float, float]

def rotate_around_centre(width: float, height: float, rotation: float) -> coords:
    """
    DOES NOT WORK. Different solution to rotation has been implemented.
    Based upon the previous width and height, and the amount the image is being rotated this function
    finds the amount that the image needs to be moved inorder to maintain the centre's position.
    """
    """
    if rotation >= 0:
        rotation = rotation%(math.pi/2)
    else:
        rotation = -(rotation%(math.pi/2))
    """

    # '1' is just a hardcoded math.sin(math.pi/2).
    A: float = math.sin(math.pi/2 - rotation)/(1/height) + math.sin(rotation)/(1/width)
    B: float = math.sin(rotation)/(1/height) + math.sin(math.pi/2 - rotation)/(1/width)
    print(f"A: {A}, B: {B}")
    return (width/2 - A/2, height/2 - B/2)
