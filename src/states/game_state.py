class GameState():
    """A class intended to handle different Game States."""

    def __init__(self, game):
        self.game = game

    def enter(self):
        """Called when entering the state."""
        pass

    def exit(self):
        """Called when exiting the state."""
        pass

    def update(self):
        """Called whenever updating the state."""
        pass

    def render(self):
        """Called whenever rendering the state."""
        pass

    def handle_event(self):
        """Called whenever an event needs to be handled."""
        pass
