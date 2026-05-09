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
        # visual parry effects: list of dicts {dir, t, dur}
        self._parries = []
        # visual stab effects: list of dicts {t, dur}
        self._stabs = []

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
        # update parry timers
        for p in list(self._parries):
            p['t'] += dt
            if p['t'] >= p['dur']:
                try:
                    self._parries.remove(p)
                except ValueError:
                    pass
        # update stabs
        for s in list(self._stabs):
            s['t'] += dt
            if s['t'] >= s['dur']:
                try:
                    self._stabs.remove(s)
                except ValueError:
                    pass

    def compute_parry_rect(self, direction, prog=0.0):
        """Return the parry hitbox Rect for `direction` at progress `prog` (0..1)."""
        if direction not in ('up', 'down'):
            return None
        w = int(self.w * 2)
        h = int(self.h * 0.6)
        # position in front of the player (to the right)
        x = int(self.x + self.w / 2)
        if direction == 'up':
            y_off = int(-prog * (self.h + 20))
        else:
            y_off = int(prog * (self.h + 20))
        y = int(self.y - h / 2 + y_off)
        return pygame.Rect(x, y, w, h)

    def compute_stab_rect(self, prog=0.0):
        """Return the stab hitbox Rect in front of the player at progress 0..1.

        The stab is a short rectangular strike in front of the player.
        """
        w = int(self.w * 1.6)
        h = int(self.h * 0.5)
        # position a little ahead of player center
        x = int(self.x + self.w / 2)
        # small forward/back motion during the stab (prog 0..1)
        reach = int(self.w * 0.6)
        x += int(prog * reach)
        y = int(self.y - h / 2)
        return pygame.Rect(x, y, w, h)

    def stab(self, balls):
        # use stab hitbox for collision when stabbing
        stab_rect = self.compute_stab_rect(prog=0.0)
        for b in list(balls):
            if b.alive and stab_rect.colliderect(b.get_rect()):
                b.on_caught(self)
                b.alive = False

    def start_stab(self):
        """Start a short visual stab effect and used hitbox for collisions."""
        self._stabs.append({'t': 0.0, 'dur': 0.12})

    def start_parry(self, direction):
        """Start a short visual parry effect. `direction` is 'up' or 'down'."""
        if direction not in ('up', 'down'):
            return
        self._parries.append({'dir': direction, 't': 0.0, 'dur': 0.28})

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 255), self.rect)
        # draw parry swipes
        for p in self._parries:
            prog = p['t'] / p['dur']
            alpha = int(255 * (1.0 - prog))
            surf = pygame.Surface((self.w * 2, int(self.h * 0.6)), pygame.SRCALPHA)
            color = (255, 255, 255, alpha)
            rect = self.compute_parry_rect(p['dir'], prog)
            if rect:
                pygame.draw.rect(surf, color, pygame.Rect(0, 0, rect.width, rect.height))
                screen.blit(surf, (rect.x, rect.y))
        # draw stabs (visual indicator matching stab hitbox)
        for s in list(self._stabs):
            prog = s['t'] / s['dur']
            alpha = int(220 * (1.0 - prog))
            rect = self.compute_stab_rect(prog)
            surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            color = (255, 200, 60, alpha)
            pygame.draw.rect(surf, color, pygame.Rect(0, 0, rect.width, rect.height))
            screen.blit(surf, (rect.x, rect.y))
