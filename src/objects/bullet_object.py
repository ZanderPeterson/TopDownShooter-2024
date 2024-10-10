from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import check_reflection, move_by_vector

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class BulletObject(GameObject):
    """A Subclass of GameObject which is intended to be used for projectiles."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 speed: float | None = None,
                 image: str | None = None) -> None:
        super().__init__(tag="bullet", start_pos=start_pos, rotation=rotation, image=image)
        if not speed:
            speed = 0
        self.speed: float = speed

    def get_vector(self) -> Vector:
        """Returns a vector which is just the (rotation, speed)"""
        return (self.speed, self.rotation)

    def update(self, walls) -> None:
        """Moved the bullet  by its speed and rotation."""
        current_pos: coords = self.position
        travel_by: Vector = self.get_vector()
        first_iteration: bool = True
        closest_wall: Tuple[int, Tuple[coords, Vector]] | None = None

        while closest_wall or first_iteration:
            first_iteration = False
            closest_wall = None

            for i, wall in enumerate(walls):
                collision_data: Tuple[coords, Vector] = check_reflection(wall.position, wall.rotation, wall.img_size,
                                                                         current_pos, travel_by)
                #If there is no collision, check next wall
                if not collision_data:
                    continue

                #If this is the first wall to have a detected collision, use this.
                if not closest_wall:
                    closest_wall = (i, collision_data)

                #If this collision is closer, store this one instead.
                if collision_data[1][0] > closest_wall[1][1][0]:
                    closest_wall = (i, collision_data)

            if not closest_wall:
                self.position = move_by_vector(current_pos, travel_by)
                self.rotation = travel_by[1]
                break

            self.position = closest_wall[1][0]
            current_pos = self.position
            travel_by = closest_wall[1][1]
