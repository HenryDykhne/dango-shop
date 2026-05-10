import os
import pygame
from dango.settings import SCREEN_W, SCREEN_H

_UI_ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets', 'ui-assets')


class CreditsScene:

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 28)

        self.border = pygame.image.load(os.path.join(_UI_ASSETS, 'credits_border.png')).convert_alpha()
        self.banner = pygame.image.load(os.path.join(_UI_ASSETS, 'credits_banner.png')).convert_alpha()

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q, pygame.K_RETURN):
                    from dango.scenes.level_select import LevelSelect
                    manager.switch(LevelSelect())

    def update(self, dt, manager):
        pass

    def draw(self, screen):
        border_x = SCREEN_W // 2 - self.border.get_width() // 2
        border_y = SCREEN_H // 2 - self.border.get_height() // 2
        screen.blit(self.border, (border_x, border_y))

        banner_x = SCREEN_W // 2 - self.banner.get_width() // 2
        screen.blit(self.banner, (banner_x, border_y + 20))

        hint = self.font.render("Press Esc / Enter to return", True, (120, 120, 120))
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 50))
