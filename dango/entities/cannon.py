import math
import random
import pygame
from dango.entities.ball import PinkBall, WhiteBall, GreenBall, BrownBall, WasabiHazard, CoalHazard, YellowBall
from dango.settings import COAL_SPREAD_OFFSET, SCREEN_W


class Cannon:
    def __init__(self):
        # placed on the right side; fires left
        self.x = SCREEN_W - 50
        self.y = 360
        self.angle = 180  # degrees: 180 => left
        self.time = 0.0
        self._since = 0.0

    def update(self, dt, queue, volley_gap):
        """Advance cannon angle and optionally fire when timer passes.

        If `queue` and `volley_gap` are provided, the cannon will pop from
        the queue and spawn a ball every `volley_gap` seconds. Returns a
        list of spawned balls (may be empty).
        """
        self.time += dt
        # oscillate angle slightly
        self.angle = 180 + math.sin(self.time * 0.4) * 45

        spawned = []
        self._since += dt
        if self._since >= volley_gap:
            self._since -= volley_gap
            # fire ball from queue
            c = queue.pop()
            if c:
                spawned.extend(self._spawn_balls(c))
        return spawned

    def _spawn_balls(self, color_key):
        # spawn at cannon position and set velocity based on angle
        rad = math.radians(self.angle)
        balls = []
        if color_key == "pink":
            balls.append(PinkBall(self.x, self.y, rad))
        elif color_key == "white":
            balls.append(WhiteBall(self.x, self.y, rad))
        elif color_key == "green":
            balls.append(GreenBall(self.x, self.y, rad))
        elif color_key == "yellow":
            balls.append(YellowBall(self.x, self.y, rad))
        elif color_key == "brown":
            balls.append(BrownBall(self.x, self.y, rad))
        elif color_key == "wasabi":
            balls.append(WasabiHazard(self.x, self.y, rad))
        elif color_key == "coal":
            offset_rad = math.radians(COAL_SPREAD_OFFSET)
            balls.append(CoalHazard(self.x, self.y, rad))
            balls.append(CoalHazard(self.x, self.y, rad + offset_rad))
            balls.append(CoalHazard(self.x, self.y, rad - offset_rad))

        return balls

    def draw(self, screen):
        # simple cannon base
        pygame.draw.rect(screen, (150, 100, 60), (self.x - 20, self.y - 10, 40, 20))
        # draw barrel rotated to `self.angle`
        rad = math.radians(self.angle)
        length = 60
        end_x = int(self.x + math.cos(rad) * length)
        end_y = int(self.y + math.sin(rad) * length)
        pygame.draw.line(screen, (200, 160, 120), (int(self.x), int(self.y)), (end_x, end_y), 6)
