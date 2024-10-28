from typing import override

import pygame

from .game_state import GameState

class MainMenuState(GameState):
    """A Subclass of GameState intended to handle the Main Menu."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.score: int = 0
        self.h1: pygame.font.FontType = pygame.font.Font(None, 80)
        self.h2: pygame.font.FontType = pygame.font.Font(None, 50)
        self.h3: pygame.font.FontType = pygame.font.Font(None, 30)

    @override
    def enter(self) -> None:
        print("Entering the Main Menu state.")

    @override
    def exit(self) -> None:
        print("Exiting the Main Menu state.")

    @override
    def render(self, window) -> None:
        window.fill((0, 0, 0))

        score_text = self.h1.render(f"Score: {self.score}", True, (255, 255, 255))
        window.blit(score_text, (400 - score_text.get_size()[0] / 2, 280 - score_text.get_size()[1] / 2))

    @override
    def handle_event(self, event) -> None | str:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("Spacebar hit")
            return "PlayGame"
        return None
