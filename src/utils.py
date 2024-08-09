# This file is for functions I might need, such as Vector Mathematics

import math

from typing import Tuple, TypeAlias

coords: TypeAlias = Tuple[float, float]

def rotate_around_centre(width: float, height: float, rotation: float) -> coords:
    """
    Based upon the previous width and height, and the amount the image is being rotated this function
    finds the amount that the image needs to be moved inorder to maintain the centre's position.
    """
    #'1' is just a hardcoded math.sin(math.pi/2).
    A: float = math.sin(math.pi/2 - rotation)/(1/height) + math.sin(rotation)/(1/width)
    B: float = math.sin(rotation)/(1/height) + math.sin(math.pi/2 - rotation)/(1/height)
    return (A/2 - width/2, B/2 - height/2)
