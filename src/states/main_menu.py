from typing import override

import pygame

from .game_state import GameState
from src.settings import Settings

class MainMenuState(GameState):
    """A Subclass of GameState intended to handle the Main Menu."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self.score: int = 0
        self.high_score: int = 0
        self.h1: pygame.font.FontType = pygame.font.Font(None, 60)
        self.h2: pygame.font.FontType = pygame.font.Font(None, 40)
        self.h3: pygame.font.FontType = pygame.font.Font(None, 20)

    @override
    def enter(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score

    @override
    def exit(self) -> None:
        pass

    @override
    def render(self, window) -> None:
        window.fill((0, 0, 0))

        title_text = self.h1.render(str(Settings.WINDOW_CAPTION), True, (254, 255, 240))
        subtitle_text = self.h3.render("Created by Zander Peterson - Version 1.0", True, (254, 255, 240))
        score_text = self.h2.render(f"Previous Score: {self.score}", True, (254, 255, 240))
        high_score_text = self.h2.render(f"Highest Score: {self.high_score}", True, (254, 255, 240))
        how_to_text = self.h1.render("Press [Space] To Start", True, (254, 255, 240))

        window.blit(title_text, (400 - title_text.get_size()[0] / 2, 100 - title_text.get_size()[1] / 2))
        window.blit(subtitle_text, (400 - subtitle_text.get_size()[0] / 2, 130 - subtitle_text.get_size()[1] / 2))
        window.blit(score_text, (400 - score_text.get_size()[0] / 2, 275 - score_text.get_size()[1] / 2))
        window.blit(high_score_text, (400 - high_score_text.get_size()[0] / 2, 325 - high_score_text.get_size()[1] / 2))
        window.blit(how_to_text, (400 - how_to_text.get_size()[0] / 2, 500 - how_to_text.get_size()[1] / 2))

    @override
    def handle_event(self, event) -> None | str:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return "PlayGame"
        return None
