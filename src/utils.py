# This file is for functions I might need, such as Vector Mathematics

import math

from typing import Tuple, TypeAlias

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction

def find_vector_between(from_pos: coords, to_pos: coords) -> Vector:
    """
    Takes two coordinates, and finds the Vector that is required to travel from
    the first Coordinate to the other Coordinate. That Vector is then returned.
    """
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
    """
    Returns a new set of coordinates based on if something at a starting
    position moves by a Vector.
    """
    return ((from_pos[0] + by_vector[0]*math.cos(by_vector[1])),
            (from_pos[1] + by_vector[0]*math.sin(-by_vector[1])))

def orbit_around_circle(old_pos: coords, pos_to_centre: Vector, orbit_by: float) -> coords:
    """
    Takes in the position of the object, and the vector from said object to the centre of the
    intended orbit, and how many pixels the object should orbit around, and returns the new
    position for the object.
    """
    orbit_by_angle: float = orbit_by/pos_to_centre[0]
    center_position: coords = move_by_vector(old_pos, pos_to_centre)
    new_position: coords = move_by_vector(center_position,
                                         (pos_to_centre[0], pos_to_centre[1] + orbit_by_angle + math.pi))

    return new_position

def reverse_vector(vector_to_reverse: Vector) -> Vector:
    """Takes in a vector, and then adds pi radians to the direction, thus reversing the direction."""
    return (vector_to_reverse[0],
            vector_to_reverse[1] + math.pi)
