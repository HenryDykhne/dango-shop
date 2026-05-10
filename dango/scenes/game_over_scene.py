import os
import pygame
from dango.settings import SCREEN_W, SCREEN_H, current_score

_UI_ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets', 'ui-assets')


class GameOverScene:

    def __init__(self, day):
        self.day = day
        self.final_score = current_score()
        self.font = pygame.font.SysFont("arial", 36)

        self.banner = pygame.image.load(os.path.join(_UI_ASSETS, 'game_over.png')).convert_alpha()
        self.btn_retry = pygame.image.load(os.path.join(_UI_ASSETS, 'btn_retry.png')).convert_alpha()
        self.btn_quit = pygame.image.load(os.path.join(_UI_ASSETS, 'btn_quit.png')).convert_alpha()

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    from dango.scenes.game_scene import GameScene
                    manager.switch(GameScene(day=self.day))
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    from dango.scenes.level_select import LevelSelect
                    manager.switch(LevelSelect())

    def update(self, dt, manager):
        pass

    def draw(self, screen):
        banner_x = SCREEN_W // 2 - self.banner.get_width() // 2
        screen.blit(self.banner, (banner_x, 150))

        score_text = self.font.render(f"Final Score: {self.final_score}¥", True, (255, 220, 180))
        screen.blit(score_text, (SCREEN_W // 2 - score_text.get_width() // 2, 260))

        retry_x = SCREEN_W // 2 - self.btn_retry.get_width() // 2
        screen.blit(self.btn_retry, (retry_x, 380))

        quit_x = SCREEN_W // 2 - self.btn_quit.get_width() // 2
        screen.blit(self.btn_quit, (quit_x, 460))

        hint = self.font.render("R retry | Q/Esc quit to menu", True, (120, 120, 120))
        screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 560))
