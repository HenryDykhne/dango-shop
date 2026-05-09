import random

# Screen
SCREEN_W, SCREEN_H = 1280, 720
FPS = 60

# Play field
FIELD_TOP = 100
FIELD_BOTTOM = 620

# Ball
BALL_RADIUS = 20
BALL_COLORS = {
    "pink":   (255, 182, 193),
    "white":  (240, 240, 240),
    "green":  (144, 238, 144),
    "yellow": (255, 215, 0),
    "brown":  (160, 82, 45),
    "orange": (255, 140, 0),
    "purple": (147, 112, 219),
    "black":  (24, 24, 24),
    "wasabi": (50, 205, 50),
    "coal":   (200, 80, 0),
}
BALL_SPEED = {
    "pink":   200,
    "white":  340,
    "green":  260,
    "yellow": 180,
    "brown":  180,
    "orange": 220,
    "purple": 260,
    "black":  260,
    "wasabi": 260,
    "coal":   260,
}

# Green ball behavior
GREEN_ACCEL = 600.0
GREEN_MID_THRESHOLD = 50.0

# Yen
BALL_VALUE = {
    "pink":  50,
    "white": 50,
    "green": 50,
    "yellow": 100,
    "brown":  100,
    "orange": 150,
    "purple": 150,
    "black":  250,
    "wasabi": 0,
    "coal":  0,
}
PENALTY = 50

# Day configs (from architecture.md)
DAYS = [
    {
        "bag":        {"pink": 4, "white": 4},
        "stick_size": 2,
        "quota":      2000,
        "volley_gap": 3.0,
    },
    {
        "bag":        {"pink": 4, "white": 4, "green": 3},
        "stick_size": 3,
        "quota":      2500,
        "volley_gap": 2.5,
    },
    {
        "bag":        {"pink": 4, "white": 4, "green": 3, "wasabi": 1},
        "stick_size": 3,
        "quota":      3000,
        "volley_gap": 2.5,
    },
]
