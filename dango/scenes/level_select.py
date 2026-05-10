import pygame
from dango.scenes.game_scene import GameScene
from dango.settings import SCREEN_W, DAYS, BALL_COLORS, SCREEN_H

BALL_RADIUS = 10

BALL_INFO = [
    ("pink",   "Dango move slowly"),
    ("white",  "Dango move faster"),
    ("green",  "Dango move in a wavy pattern"),
    ("yellow", "Dango will home in on you"),
    ("brown",  "Dango will avoid you"),
    ("orange", "Dango slow to a stop and then accelerate"),
    ("wasabi", "Hazard — scrambles your controls briefly"),
    ("coal",   "Hazard — destroys all dango on your stick"),
]

CONTROLS = [
    ("WASD",       "Move"),
    ("SPACE",      "Stab ball onto stick"),
    ("H",          "Parry up — sends ball to front of queue"),
    ("J",          "Parry down — sends ball to bag"),
    ("SHIFT",      "Dash"),
]

class LevelSelect:
    def __init__(self):
        self.selected = 0
        self.font_title    = pygame.font.SysFont("arial", 56)
        self.font_subtitle = pygame.font.SysFont("arial", 18)
        self.font_item     = pygame.font.SysFont("arial", 36)
        self.font_section  = pygame.font.SysFont("arial", 20, bold=True)
        self.font_body     = pygame.font.SysFont("arial", 17)

        # layout constants
        self.LEFT_W  = SCREEN_W // 2          # left panel width
        self.RIGHT_X = SCREEN_W // 2 + 20     # right panel start x
        self.RIGHT_W = SCREEN_W // 2 - 40     # right panel width
        self.BOX_X   = self.RIGHT_X - 10
        self.BOX_Y   = 100
        self.BOX_W   = self.RIGHT_W + 10
        self.BOX_H   = SCREEN_H - 140

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    self.selected = (self.selected - 1) % len(DAYS)
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    self.selected = (self.selected + 1) % len(DAYS)
                if event.key == pygame.K_RETURN:
                    manager.switch(GameScene(day=self.selected + 1))

    def update(self, dt, manager):
        pass

    def _draw_section(self, screen, label, y):
        surf = self.font_section.render(label, True, (255, 220, 180))
        screen.blit(surf, (self.RIGHT_X, y))
        return y + surf.get_height() + 4

    def draw(self, screen):
        # ── left panel ──────────────────────────────────────────────
        title = self.font_title.render("Dango Shop", True, (255, 220, 180))
        screen.blit(title, (self.LEFT_W // 2 - title.get_width() // 2, 30))

        subtitle = self.font_subtitle.render(
            "by Henry Dykhne, Alon Djurinsky and Kajal Panicker for ToJam 2026!",
            True, (255, 220, 180)
        )
        screen.blit(subtitle, (self.LEFT_W // 2 - subtitle.get_width() // 2, 100))

        for idx in range(len(DAYS)):
            color = (255, 255, 100) if idx == self.selected else (180, 180, 180)
            text = self.font_item.render(f"Day {idx + 1}", True, color)
            screen.blit(text, (self.LEFT_W // 2 - text.get_width() // 2, 160 + idx * 60))

        hint = self.font_body.render("W/S to select   Enter to start", True, (120, 120, 120))
        screen.blit(hint, (self.LEFT_W // 2 - hint.get_width() // 2, SCREEN_H - 60))

        # ── right panel box ─────────────────────────────────────────
        box_surf = pygame.Surface((self.BOX_W, self.BOX_H), pygame.SRCALPHA)
        pygame.draw.rect(box_surf, (255, 255, 255, 18), (0, 0, self.BOX_W, self.BOX_H), border_radius=10)
        pygame.draw.rect(box_surf, (255, 220, 180, 60), (0, 0, self.BOX_W, self.BOX_H), width=1, border_radius=10)
        screen.blit(box_surf, (self.BOX_X, self.BOX_Y))

        y = self.BOX_Y + 14
        pad = self.RIGHT_X + 6

        # ── how to win ──────────────────────────────────────────────
        y = self._draw_section(screen, "How to Win", y)
        for line in (
            "* Meet the day's quota before time runs out.",
            "* Match customers' orders by ball color (order doesn't matter).",
            "* Completed sticks are served automatically, or held in the display rack until",
            "  a matching customer arrives.",
            "* Don't get hit by dango or let them hit the backstop, or you'll lose points!",
        ):
            s = self.font_body.render(line, True, (210, 210, 210))
            screen.blit(s, (pad, y))
            y += s.get_height() + 2
        y += 10

        # ── controls ────────────────────────────────────────────────
        y = self._draw_section(screen, "Controls", y)
        key_font = pygame.font.SysFont("arial", 17, bold=True)
        for key, desc in CONTROLS:
            key_surf = key_font.render(f"{key}", True, (255, 220, 100))
            desc_surf = self.font_body.render(f"  {desc}", True, (210, 210, 210))
            screen.blit(key_surf, (pad, y))
            screen.blit(desc_surf, (pad + key_surf.get_width(), y))
            y += key_surf.get_height() + 3
        y += 10

        # ── balls & hazards ─────────────────────────────────────────
        y = self._draw_section(screen, "Balls & Hazards", y)
        for color_key, desc in BALL_INFO:
            color = BALL_COLORS[color_key]
            # draw example ball
            pygame.draw.circle(screen, color, (pad + BALL_RADIUS, y + BALL_RADIUS), BALL_RADIUS)
            if color_key == "white":
                pygame.draw.circle(screen, (150, 150, 150), (pad + BALL_RADIUS, y + BALL_RADIUS), BALL_RADIUS, 1)
            label = self.font_body.render(f"  {color_key.capitalize()} {desc}", True, (210, 210, 210))
            screen.blit(label, (pad + BALL_RADIUS * 2 + 4, y + BALL_RADIUS - label.get_height() // 2))
            y += BALL_RADIUS * 2 + 6