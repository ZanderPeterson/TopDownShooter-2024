from typing import Tuple, TypeAlias

import pygame

from .game_object import GameObject
from src.utils import check_reflection, move_by_vector, find_vector_between

coords: TypeAlias = Tuple[float, float]
Vector: TypeAlias = Tuple[float, float] #Magnitude, Direction


class BulletObject(GameObject):
    """A Subclass of GameObject which is intended to be used for projectiles."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 speed: float | None = None,
                 shot_by: str | None = None,
                 grace_period: int = 0,
                 image: str | None = None) -> None:
        super().__init__(tag="bullet", start_pos=start_pos, rotation=rotation, image=image)
        if not speed:
            speed = 0
        self.speed: float = speed
        self.shot_by: str | None = shot_by
        self.grace_period: int = grace_period

    def get_vector(self) -> Vector:
        """Returns a vector which is just the (rotation, speed)"""
        return (self.speed, self.rotation)

    def update(self, walls: list[GameObject], targets: list[GameObject]) -> list[GameObject]:
        """
        Moved the bullet  by its speed and rotation.
        Also calculates the reflections off walls.
        Also returns any objects that the bullet is colliding with.
        """
        current_pos: coords = self.get_centre_position()
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
                self.set_position_by_centre(move_by_vector(current_pos, travel_by))
                self.rotation = travel_by[1]
                break

            travel_by = closest_wall[1][1]
            self.set_position_by_centre(move_by_vector(closest_wall[1][0], by_vector=(0.1, travel_by[1])))
            current_pos = self.get_centre_position()

        targets_hit: list[GameObject] = []
        for target in targets:
            distance_to_target: float = find_vector_between(self.get_centre_position(), target.get_centre_position())[0]

            #Sets the target radius, which determines the size of the hitbox.
            #Players get a small advantage with having a slightly smaller hitbox,
            #Whilst enemies get a small disadvantage with having a slightly bigger one.
            #Making things more forgiving for players makes the game feel better and fairer.
            target_radius: float = (target.img_size[0]/2)*1.5
            if target.tag == "player":
                target_radius = (target.img_size[0]/2)*0.8

            if distance_to_target >= target_radius:
                continue
            if (target.tag == self.shot_by or self.shot_by is None) and self.grace_period > 0:
                #Grace period applies. Target is not hit.
                continue
            targets_hit.append(target)

        self.grace_period = max(self.grace_period - 1, 0)
        return targets_hit
