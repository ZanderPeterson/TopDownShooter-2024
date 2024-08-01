# This file handles the running of the game and the differing game states.

import pygame

from states.main_menu import MainMenuState

class Game():
    """A Class intended to handle game related functions."""

    def __init__(self, window) -> None:
        self.window = window
        self.states = {
            "main_menu": MainMenuState(self)
        }
        self.current_state = self.states["main_menu"]
        self.current_state.enter()

    def change_state(self, to_state: str) -> None:
        self.current_state.exit()
        self.current_state = self.states[to_state]
        self.current_state.enter()

    def handle_event(self, event) -> None:
        self.current_state.handle_event(event)

    def update(self) -> None:
        self.current_state.update()

    def render(self) -> None:
        self.current_state.render(self.window)
