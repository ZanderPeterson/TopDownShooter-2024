# This file is for functions I might need, such as Vector Mathematics

import math
import random

from typing import Callable, List, Tuple, TypeAlias

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
    return (side_length / 2) / max(abs(math.cos(rotation)), abs(math.sin(rotation)))

def check_collision(still_obj_pos: coords, still_obj_radius_func: Callable[[float], float],
                    moving_obj_pos: coords, moving_obj_radius_func: Callable[[float], float]) -> Vector:
    """
    This function takes in the still_obj's centre position and a function that takes in an angle in radians
    and a moving_obj's position and radius calculating function.

    Some examples of acceptable inputs for still_obj_radius_func would be:
    lambda theta: find_radius_of_square(32, theta-(1.04))
    lambda theta: 16

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
    return reverse_vector((-space_between_objects, vector_between_centres[1]))

def find_line_intersection(line_a: Tuple[coords, coords],
                           line_b: Tuple[coords, coords]) -> Tuple[coords, bool, float, float] | None:
    """
    Takes in two lines (A line is described as 2 positions) and outputs some values.

    If the lines are parallel or collinear, then the output is None.
    These values are the intersection point (which will always give a value, even if
    the lines do not intersect), A bool which describes if there is a collision, and 2 floats.

    The first float is where along the first line the intersection occurs (ranges from
    0-1 if colliding, may be another value if no collision) and the second float is
    the same deal but along the second line.
    """
    #This may slightly hurt execution speed, but significantly aids in readability.
    point_a: coords = line_a[0]
    point_b: coords = line_a[1]
    point_c: coords = line_b[0]
    point_d: coords = line_b[1]

    #Determinate calculations
    determinate: float = ((point_b[0] - point_a[0])*(point_d[1] - point_c[1])
                         -(point_b[1] - point_a[1])*(point_d[0] - point_c[0]))
    if determinate == 0:
        return None #Lines are parallel or collinear.

    #Calculations that determine where on the lines the intersection occurs.
    line_a_intersection: float = ((point_c[0] - point_a[0])*(point_d[1] - point_c[1])
                                 -(point_c[1] - point_a[1])*(point_d[0] - point_c[0]))/determinate
    line_b_intersection: float = ((point_c[0] - point_a[0])*(point_b[1] - point_a[1])
                                 -(point_c[1] - point_a[1])*(point_b[0] - point_a[0]))/determinate

    #Calculates the intersection point
    intersection_point: coords = (point_a[0] + line_a_intersection*(point_b[0] - point_a[0]),
                                  point_a[1] + line_a_intersection*(point_b[1] - point_a[1]))

    #Returns all the information required, as explained in the documentation.
    return (intersection_point,
            0 <= line_a_intersection <= 1 and 0 <= line_b_intersection <= 1,
            line_a_intersection,
            line_b_intersection)

def check_reflection(wall_obj_pos: coords, wall_obj_rotation: float, wall_obj_size: Tuple[float, float],
                     bullet_pos: coords, bullet_travel_by: Vector) -> Tuple[coords, Vector] | None:
    """
    This function takes in some data from a wall object (Corner Position, Rotation,
    and Shape Size (not accounting for rotation) and some data from a bullet object
    (Bullet Position & its move_by Vector).

    It then returns a coordinate and a Vector. The Coordinate is the point of collision,
    whilst the Vector is what is needed to be traveled to get to the new position. It may
    return None in the case that no collision occurs.
    """
    wall_obj_centre: coords = (wall_obj_pos[0] + wall_obj_size[0],
                               wall_obj_pos[1] + wall_obj_size[1])
    wall_obj_pos_to_centre: Vector = find_vector_between(wall_obj_pos, wall_obj_centre)
    wall_obj_corner: coords = find_object_corner(wall_obj_pos, wall_obj_pos_to_centre, wall_obj_rotation)

    bullet_line: Tuple[coords, coords] = (bullet_pos, move_by_vector(bullet_pos, bullet_travel_by))

    old_corner: coords = (wall_obj_corner[0], wall_obj_corner[1]+wall_obj_size[1])
    collision_results: List[Tuple[coords, bool, float, float] | None] = []
    wall_corner_positions: List[coords] = []

    #Iterate over all the sides and record any collisions between the bullet and that side.
    for side in range(0, 4):
        wall_corner_positions.append(old_corner)
        side_vector: Vector = (wall_obj_size[side%2], side*(math.pi/2) + wall_obj_rotation)
        new_corner: coords = move_by_vector(old_corner, side_vector)
        line: Tuple[coords, coords] = (old_corner, new_corner)
        collision_results.append(find_line_intersection(line, bullet_line))
        old_corner = new_corner

    #This fuss over the 'closest_collision' helps make the code more robust and less error-prone.
    #This is because the bullet may intersect over multiple sides. In that edge case, the bullet should
    #In that situation, the bullet should reflect off the first side it would have encountered.
    closest_collision: int | None = None
    for i, collision in enumerate(collision_results):
        if not collision:  #If this collision is parallel or collinear
            continue
        if not collision[1]:  #If this collision occurs outside the lines.
            continue

        if not closest_collision:  #If this is the first collision
            closest_collision = i
        elif collision_results[closest_collision][3] > collision[3]:  #See if this collision is closer.
            closest_collision = i

    if closest_collision is None: #If there were no collisions at all
        return None

    #This code will only be executed if there was a collision.
    collision: Tuple[coords, bool, float, float] = collision_results[closest_collision]
    point_a: coords = wall_corner_positions[closest_collision - 1]
    point_b: coords = wall_corner_positions[closest_collision]
    side_length: float = wall_obj_size[closest_collision%2]

    #Determine the closest point, which is needed for reflection calculations.
    point_a_distance_from_bullet: float = find_vector_between(bullet_pos, point_a)[0]
    point_b_distance_from_bullet: float = find_vector_between(bullet_pos, point_b)[0]
    if point_a_distance_from_bullet < point_b_distance_from_bullet:
        closest_corner: coords = point_a
        closest_side: float = side_length*(1 - collision[2])
        add_or_sub: int = -1
    else:
        closest_corner: coords = point_b
        closest_side: float = side_length*collision[2]
        add_or_sub: int = 1

    #Reflection Calculations
    bullet_travel_before_collision: float = bullet_travel_by[0]*collision[3]
    bullet_travel_after_collision: float = bullet_travel_by[0] - bullet_travel_before_collision
    opposite: float = find_vector_between(closest_corner, bullet_pos)[0]
    angle_of_incidence: float = math.pi/2 - math.acos((bullet_travel_before_collision**2 + closest_side**2 - opposite**2)/(2*bullet_travel_before_collision*closest_side))
    reflected_ray: float = (bullet_travel_by[1] + angle_of_incidence*2*add_or_sub + math.pi)%(2*math.pi)
    return (collision[0], (bullet_travel_after_collision, reflected_ray))

def random_normal(min_value: float, max_value: float, mean: float, deviation: float, max_tries: int = 10) -> float:
    """
    Generates a pseudo-random normal distribution.
    Unstable behaviour may be caused if the mean fails to fall between min_value & max_value.
    If max_tries is reached, it instead returns a triangular distribution.
    """
    for i in range(1, max_tries):
        random_number: float = random.gauss(mean, deviation)
        if min_value <= random_number <= max_value:
            return random_number
    #If it gave up:
    return random.triangular(min_value, max_value, mean)
