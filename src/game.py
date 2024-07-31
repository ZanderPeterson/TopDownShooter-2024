# This file handles the running of the game and the differing game states.

import pygame

class Game():
    """A Class intended to handle game related functions."""

    def __init__(self, window):
        self.window = window
        self.states = {}
