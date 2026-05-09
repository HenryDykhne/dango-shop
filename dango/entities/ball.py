import math
import pygame
from dango.settings import AVOIDANCE_ACCEL, AVOIDANCE_SPEED_MULTIPLIER, BALL_RADIUS, BALL_COLORS, BALL_SPEED, BALL_VALUE, FIELD_TOP, FIELD_BOTTOM, GREEN_ACCEL, GREEN_MID_THRESHOLD, HOMING_ACCEL, HOMING_SPEED_MULTIPLIER


class Ball:
    """Base ball. Initialize with an angle (radians) and initial speed.

    Angle is in radians (0 = right, pi = left). The cannon will pass the
    launch angle when creating balls.
    """
    color = (255, 255, 255)
    speed = 200
    value = 0
    is_hazard = False

    def __init__(self, x, y, angle_rad, color_key):
        self.x = float(x)
        self.y = float(y)
        self.origin_y = y
        self.radius = BALL_RADIUS
        self.alive = True

        # preserve the color key for gameplay systems (queue, parry, bag)
        self.color_key = color_key
        self.color = BALL_COLORS.get(color_key, self.color)
        self.value = BALL_VALUE.get(color_key, 0)
        # set per-color initial speed if available
        self.speed = BALL_SPEED.get(color_key, self.speed)

        # velocity from angle and speed
        self.vx = math.cos(angle_rad) * self.speed
        self.vy = math.sin(angle_rad) * self.speed

    def update(self, dt, player):
        # default: straight-line motion (accept optional player object)
        self.x += self.vx * dt
        self.y += self.vy * dt

        # bounce off top/bottom
        self._bounce()


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def _bounce(self):
        """Bounce the ball off the playfield top/bottom and flip vertical velocity."""
        if self.y - self.radius <= FIELD_TOP:
            self.y = FIELD_TOP + self.radius
            self.vy *= -1
        if self.y + self.radius >= FIELD_BOTTOM:
            self.y = FIELD_BOTTOM - self.radius
            self.vy *= -1

    def on_parried_up(self):
        pass

    def on_parried_down(self):
        pass


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

    def update(self, dt, player):
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
        self._bounce()

class BrownBall(Ball):
    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="brown")

    def update(self, dt, player):
         # forward motion
        self.x += self.vx * dt

        # if we have the player's object, accelerate vertically away from them to dodge them.

        # scale speed by distance (closer -> faster)
        targetvy = AVOIDANCE_SPEED_MULTIPLIER * (1 - (abs(self.y - player.y) / (FIELD_BOTTOM - FIELD_TOP)))
        if self.y < player.y:
            targetvy = -targetvy

        if targetvy > self.vy:
            self.vy += AVOIDANCE_ACCEL * dt
        else:
            self.vy -= AVOIDANCE_ACCEL * dt

        # apply vertical velocity
        self.y += self.vy * dt

        # bounce off top/bottom
        self._bounce()

class YellowBall(Ball):
    def __init__(self, x, y, angle_rad=math.pi):
        super().__init__(x, y, angle_rad, color_key="yellow")

    def update(self, dt, player):
        # forward motion
        self.x += self.vx * dt

        # if we have the player's object, accelerate vertically towards them to 'target' them.

        # scale speed by distance (closer -> slower)
        targetvy = HOMING_SPEED_MULTIPLIER * (player.y - self.y) / (FIELD_BOTTOM - FIELD_TOP)
        if targetvy > self.vy:
            self.vy += HOMING_ACCEL * dt
        else:
            self.vy -= HOMING_ACCEL * dt

        # apply vertical velocity
        self.y += self.vy * dt

        # bounce off top/bottom
        self._bounce()

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
