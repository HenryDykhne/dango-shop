import pygame
from dango.settings import DAYS, BALL_COLORS

class Stick:
    def __init__(self, on_complete_stick, day):
        self.max_balls = DAYS[day - 1]['stick_size']
        self.ball_keys = []
        self.on_complete_stick = on_complete_stick

    def add(self, ball_key):
        self.ball_keys.append(ball_key)
        if len(self.ball_keys) >= self.max_balls:
            self.on_complete_stick(self.ball_keys)
            self.ball_keys = []
    
    def draw(self, screen, x_offset, y_offset):
        # TODO Draw the stick here when we have the sprite for it
        radius = 6
        dx, dy = 0, radius*2 + 1
        for i, colorName in enumerate(self.ball_keys):
            color = BALL_COLORS[colorName]
            x = x_offset + dx*i
            y = y_offset + dy*i

            pygame.draw.circle(screen, color, (x, y), radius)
