# This file is for functions I might need, such as Vector Mathematics

import math

from typing import Callable, Tuple, TypeAlias

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

def find_object_corner(corner_position: coords, pos_to_centre: Vector, rotation: float) -> coords:
    """
    Finds the new corner position based upon the old corner's position,
    the centre of the sprite, and the amount the object is being rotated.
    """
    orbit_by = rotation * pos_to_centre[1]
    return orbit_around_circle(corner_position, pos_to_centre, orbit_by)

def reverse_vector(vector_to_reverse: Vector) -> Vector:
    """Takes in a vector, and then adds pi radians to the direction, thus reversing the direction."""
    return (vector_to_reverse[0],
            vector_to_reverse[1] + math.pi)

def find_radius_of_square(side_length: float, rotation: float) -> float:
    """
    Finds the distance from the middle to the right side, and accounts for rotation.
    Returned Result varies from side_length/2 to side_length*sqrt(2)/2
    """
    return side_length*sqrt(2)/2 * math.cos(rotation%(pi/2) - pi/4)

def check_collision(still_obj_pos: coords, still_obj_radius_func: Callable[[float], float],
                    moving_obj_pos: coords, moving_obj_radius_func: Callable[[float], float]) -> Vector:
    """
    This function takes in the still_obj's centre position and a function that takes in an angle in radians
    and a moving_obj's position and radius calculating function.

    Some examples of acceptable inputs for still_obj_radius_func would be:
    lambda theta: find_radius_of_square(32, theta-(1.04))
    lambda theta: 32

    If the moving obj follows the returned Vector, then the objects will no longer be colliding.
    The returned Vector is (0, 0) if there is no collision in the first place.
    """
    vector_between_centres: Vector = find_vector_between(moving_obj_pos, still_obj_pos)
    moving_obj_radius: float = moving_obj_radius_func(vector_between_centres[1])
    still_obj_radius: float = still_obj_radius_func(reverse_vector(vector_between_centres)[1])

    space_between_objects: float = vector_between_centres[0] - (moving_obj_radius + still_obj_radius)

    if space_between_objects > 0:
        #Objects are NOT colliding.
        return (0, 0)
    return reverse_vector(space_between_objects, vector_between_centres[0])
