# This file is for functions I might need, such as Vector Mathematics

import math

from typing import Tuple, TypeAlias

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction

def find_vector_between(from_pos: coords, to_pos: coords) -> Vector:
    if from_pos == to_pos:
        return (0, 0)
    x_difference: float = to_pos[0] - from_pos[0]
    y_difference: float = to_pos[1] - from_pos[1]
    magnitude: float = abs(math.sqrt(x_difference**2 + y_difference**2))
    if y_difference <= 0:
        direction: float = 2*math.pi - math.acos(x_difference / magnitude)
    else:
        direction: float = math.acos(x_difference / magnitude)
    return (magnitude, -direction)

def move_by_vector(from_pos: coords, by_vector: Vector) -> coords:
    return ((from_pos[0] + by_vector[0]*math.cos(by_vector[1])),
            -(from_pos[1] + by_vector[0]*math.sin(by_vector[1])))
