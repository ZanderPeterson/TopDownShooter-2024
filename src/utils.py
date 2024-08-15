# This file is for functions I might need, such as Vector Mathematics

import math

from typing import Tuple, TypeAlias

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction

def find_vector_between(from_pos: coords, to_pos: coords) -> Vector:
    if from_pos == to_pos:
        return (0, 0)
    x_difference = to_pos[0] - from_pos[0]
    y_difference = to_pos[1] - from_pos[1]
    magnitude = math.sqrt(x_difference**2 + y_difference**2)
    direction = math.acos(x_difference / magnitude)
    return (magnitude, direction)
