class GameState():
    """A class intended to handle different Game States."""

    def __init__(self, game) -> None:
        self.game = game

    def enter(self) -> None:
        """Called when entering the state."""
        pass

    def exit(self) -> None:
        """Called when exiting the state."""
        pass

    def update(self) -> None:
        """Called whenever updating the state."""
        pass

    def render(self) -> None:
        """Called whenever rendering the state."""
        pass

    def handle_event(self) -> None:
        """Called whenever an event needs to be handled."""
        pass
