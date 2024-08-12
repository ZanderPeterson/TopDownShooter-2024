import pygame

from .game_object import GameObject


class PlayerObject(GameObject):
    """A Subclass of GameObject which is intended to be used as the player."""

    def __init__(self,
                 start_pos: coords = (0, 0),
                 rotation: float = 0,
                 image: str | None = None) -> None:
        super().__init__(tag="player", start_pos=start_pos, rotation=rotation, image=image)
