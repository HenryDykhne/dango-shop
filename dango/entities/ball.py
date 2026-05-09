import math
import pygame
from dango.settings import BALL_RADIUS, BALL_COLORS, BALL_SPEED, BALL_VALUE, FIELD_TOP, FIELD_BOTTOM, GREEN_ACCEL, GREEN_MID_THRESHOLD


class Ball:
    """Base ball. Initialize with an angle (radians) and initial speed.

    Angle is in radians (0 = right, pi = left). The cannon will pass the
    launch angle when creating balls.
    """
    color = (255, 255, 255)
    speed = 200
    value = 0
    is_hazard = False

    def __init__(self, x, y, angle_rad=math.pi, color_key=None):
        self.x = float(x)
        self.y = float(y)
        self.origin_y = y
        self.radius = BALL_RADIUS
        self.alive = True

        self.color = BALL_COLORS.get(color_key, self.color)
        self.value = BALL_VALUE.get(color_key, 0)
        # set per-color initial speed if available
        self.speed = BALL_SPEED.get(color_key, self.speed)

        # velocity from angle and speed
        self.vx = math.cos(angle_rad) * self.speed
        self.vy = math.sin(angle_rad) * self.speed

    def update(self, dt):
        # default: straight-line motion
        self.x += self.vx * dt
        self.y += self.vy * dt

        # bounce off top/bottom
        if self.y - self.radius <= FIELD_TOP:
            self.y = FIELD_TOP + self.radius
            self.vy *= -1
        if self.y + self.radius >= FIELD_BOTTOM:
            self.y = FIELD_BOTTOM - self.radius
            self.vy *= -1


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def on_parried_up(self):
        pass

    def on_parried_down(self):
        pass

    def on_caught(self, player):
        player.stick.append(self)


class PinkBall(Ball):
    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="pink")


class WhiteBall(Ball):
    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="white")


class GreenBall(Ball):
    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="green")
        # acceleration magnitude for the yoyo behavior (from settings)
        self.accel = GREEN_ACCEL
        # threshold (px) around midpoint where we keep accelerating in current vy direction
        self.mid_threshold = GREEN_MID_THRESHOLD

    def update(self, dt):
        # forward motion
        self.x += self.vx * dt

        # accelerate toward the midpoint to create a yoyo effect
        mid = (FIELD_TOP + FIELD_BOTTOM) * 0.5
        dist = self.y - mid
        if abs(dist) > self.mid_threshold: #apply no force if close to the midpoint
            # farther from midpoint: accelerate toward it
            if self.y < mid:
                # above midpoint -> accelerate down
                self.vy += self.accel * dt
            else:
                # below midpoint -> accelerate up
                self.vy -= self.accel * dt

        # apply vertical velocity
        self.y += self.vy * dt

        # bounce off top/bottom
        if self.y - self.radius <= FIELD_TOP:
            self.y = FIELD_TOP + self.radius
            self.vy *= -1
        if self.y + self.radius >= FIELD_BOTTOM:
            self.y = FIELD_BOTTOM - self.radius
            self.vy *= -1

        if self.x < -200:
            self.alive = False


class WasabiHazard(Ball):
    is_hazard = True

    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="wasabi")

    def on_caught(self, player):
        # scramble effect placeholder
        pass


class CoalHazard(Ball):
    is_hazard = True

    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="coal")

    def on_caught(self, player):
        player.stick.clear()
