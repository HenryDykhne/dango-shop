import math
import pygame
import random
from dango.settings import DAYS, BALL_COLORS

class DangoHolders:
    def __init__(self):
        self.sticks = []
    
    def add_stick(self, stick):
        self.sticks = self.sticks[-9:] + [stick]
    
    def draw(self, screen):
        radius = 4
        for i in range(len(self.sticks)):
            stick = self.sticks[i]
            for j in range(len(stick)):
                color_key = stick[j]
                color = BALL_COLORS[color_key]

                x = 540 + i * (radius*2 + 10)
                y = 5 + radius + j*(2*radius + 1)
                pygame.draw.circle(screen, color, (x, y), radius)
