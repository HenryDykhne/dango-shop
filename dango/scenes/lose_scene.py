import os

import pygame
from dango.scenes.level_select import LevelSelect
from dango.settings import BASE_DIR, SCREEN_W, SCREEN_H

class QuotaFailScene:
    def __init__(self, score, quota):
        self.font_title = pygame.font.SysFont("arial", 42)
        self.font_sub = pygame.font.SysFont("arial", 32)
        self.font_btn = pygame.font.SysFont("arial", 28)
        self.score = score
        self.quota = quota

        try:
            raw = pygame.image.load(os.path.join(BASE_DIR, "img/TOJam_Goat.webp")).convert_alpha()
            self.image = pygame.transform.scale(raw, (176, 300))
        except Exception as e:
            self.image = None

        self.image_rect = pygame.Rect(SCREEN_W // 2 - (176/2), 200, 176, 300)

        btn_w, btn_h = 280, 50
        self.btn_rect = pygame.Rect(SCREEN_W // 2 - btn_w // 2, self.image_rect.bottom + 90, btn_w, btn_h)

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    manager.switch(LevelSelect())

    def update(self, dt, manager):
        pass

    def draw(self, screen):
        # title
        title = self.font_title.render("Day Over. You failed to meet the quota.", True, (220, 80, 80))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 110))
        result = self.font_title.render(f"¥{self.score}/¥{self.quota}", True, (220, 80, 80))
        screen.blit(result, (SCREEN_W // 2 - result.get_width() // 2, 150))

        # image
        if self.image:
            screen.blit(self.image, self.image_rect)
        else:
            pygame.draw.rect(screen, (80, 80, 80), self.image_rect)

        # subtitle
        sub = self.font_sub.render("Grandpa is disappointed.", True, (200, 200, 200))
        screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, self.image_rect.bottom + 50))

        # button
        btn_color = (100, 100, 100) if pygame.key.get_pressed()[pygame.K_RETURN] else (60, 60, 60)
        pygame.draw.rect(screen, btn_color, self.btn_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), self.btn_rect, width=1, border_radius=8)
        btn_text = self.font_btn.render("Press Enter to continue", True, (220, 220, 220))
        screen.blit(btn_text, (
            self.btn_rect.centerx - btn_text.get_width() // 2,
            self.btn_rect.centery - btn_text.get_height() // 2
        ))