import pygame
from dango.settings import FIELD_TOP, FIELD_BOTTOM


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 40
        self.h = 60
        self.speed = 300.0
        self.stick = []

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w / 2), int(self.y - self.h / 2), self.w, self.h)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        vx = 0
        vy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vx = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vy = 1
        return vx, vy

    def update(self, dt):
        vx, vy = self.handle_input()
        self.x += vx * self.speed * dt
        self.y += vy * self.speed * dt
        # clamp to field
        self.y = max(FIELD_TOP + self.h / 2, min(FIELD_BOTTOM - self.h / 2, self.y))
        self.x = max(0 + self.w / 2, min(1280 - self.w / 2, self.x))

    def stab(self, balls):
        # simple collision-based catch: nearest ball in range
        for b in list(balls):
            if b.alive and self.rect.colliderect(b.get_rect()):
                b.on_caught(self)
                b.alive = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 255), self.rect)
