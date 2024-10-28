# This file handles the running of the game and the differing game states.

import pygame

from src.states.main_menu import MainMenuState
from src.states.play_game import PlayGameState

class Game():
    """A Class intended to handle game related functions."""

    def __init__(self, window) -> None:
        self.window = window
        self.states = {
            "main_menu": MainMenuState(self),
            "play_game": PlayGameState(self)
        }
        self.current_state = self.states["main_menu"]
        self.current_state.enter()

    def change_state(self, to_state: str) -> None:
        self.current_state.exit()
        self.current_state = self.states[to_state]
        self.current_state.enter()

    def handle_event(self, event) -> None:
        returned_value: None | str = self.current_state.handle_event(event)
        if returned_value is None:
            return None
        if returned_value == "PlayGame":
            self.change_state("play_game")

    def update(self) -> None:
        returned_value: None | str = self.current_state.update()
        if returned_value is None:
            return None
        if returned_value == "GameOver":
            self.change_state("main_menu")
            self.states["main_menu"].score = self.states["play_game"].game_variables["score"]

    def render(self) -> None:
        self.current_state.render(self.window)
