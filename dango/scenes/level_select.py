import pygame
from dango.scenes.game_scene import GameScene
from dango.settings import SCREEN_W, DAYS


class LevelSelect:

    def __init__(self):
        # use `selected` as a 0-based index into `DAYS` (index 0 => Day 1)
        self.selected = 0
        self.font_title = pygame.font.SysFont("arial", 56)
        self.font_item = pygame.font.SysFont("arial", 36)

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    self.selected = (self.selected - 1) % len(DAYS)
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    self.selected = (self.selected + 1) % len(DAYS)
                if event.key == pygame.K_RETURN:
                    # pass 1-based day number
                    manager.switch(GameScene(day=self.selected + 1))

    def update(self, dt, manager):
        pass

    def draw(self, screen):
        title = self.font_title.render("Dango Shop", True, (255, 220, 180))
        screen.blit(title, (SCREEN_W // 2 - 140, 150))

        for idx in range(len(DAYS)):
            day = idx + 1
            color = (255, 255, 100) if idx == self.selected else (180, 180, 180)
            text = self.font_item.render(f"Day {day}", True, color)
            screen.blit(text, (SCREEN_W // 2 - 80, 230 + idx * 60))

        hint = self.font_item.render("W/S to select   Enter to start", True, (120, 120, 120))
        screen.blit(hint, (SCREEN_W // 2 - 220, 600))
