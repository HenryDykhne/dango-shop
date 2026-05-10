import random

# Screen
SCREEN_W, SCREEN_H = 1280, 720
BACKSTOP_WIDTH = 50
FPS = 60

# player
PLAYER_SPEED = 300.0
PLAYER_DASH_SPEED = 750.0
PLAYER_AFTERIMAGE_CD = 0.02
PLAYER_AFTERIMAGE_LEN = 0.5

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
    "coal":   (36, 26, 11),
}
BALL_SPEED = {
    "pink":   200,
    "white":  340,
    "green":  260,
    "yellow": 280,
    "brown":  280,
    "orange": 400,
    "purple": 260,
    "black":  260,
    "wasabi": 260,
    "coal":   260,
}

# Endlag
PARRY_ENDLAG_DURATION = 0.4
STAB_ENDLAG_DURATION = 0.4

# Green ball behavior
GREEN_ACCEL = 600.0
GREEN_MID_THRESHOLD = 50.0

# hazard behavior
WASABI_SCRAMBLE_DURATION = 3.0
COAL_SPREAD_OFFSET = 15.0  # degrees of spread for coal balls


# Homing Behavior for yellow and brown balls
AVOIDANCE_SPEED_MULTIPLIER = 1000.0
AVOIDANCE_ACCEL = 400.0
HOMING_SPEED_MULTIPLIER = 1000.0
HOMING_ACCEL = 600.0

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
        "bag":        {"orange": 4, "white": 4},
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
        "bag":        {"pink": 4, "white": 4, "green": 3, "yellow": 2, "wasabi": 1},
        "stick_size": 3,
        "quota":      3000,
        "volley_gap": 2.5,
    },
    {
        "bag":        {"pink": 4, "white": 4, "green": 3, "yellow": 2, "brown": 2, "wasabi": 1},
        "stick_size": 4,
        "quota":      3500,
        "volley_gap": 2.5,
    },
    {
        "bag":        {"pink":4, "white":4, "green":3, "yellow":2, "brown":2, "wasabi":1, "coal":1},
        #"bag": {"pink":4, "white":4, "green":3, "yellow":2, "brown":2, "orange":2, "wasabi":1, "coal":1}, #actual
        "stick_size": 4,
        "quota":      4000,
        "volley_gap": 2.5,
    },
]

# Additional days (commented out):
# {
#     "bag": {"pink":4, "white":4, "green":3, "yellow":2, "brown":2, "orange":2, "wasabi":1, "coal":1},
#     "stick_size": 4,
#     "quota": 4000,
#     "volley_gap": 2.5,
# },
# {
#     "bag": {"pink":4, "white":4, "green":3, "yellow":2, "brown":2, "orange":2, "purple":2, "wasabi":1, "coal":1},
#     "stick_size": 5,
#     "quota": 5000,
#     "volley_gap": 2.5,
# },
# {
#     "bag": {"pink":4, "white":4, "green":3, "yellow":2, "brown":2, "orange":2, "purple":2, "black":1, "wasabi":1, "coal":1},
#     "stick_size": 5,
#     "quota": 5500,
#     "volley_gap": 2.5,
# },


def init_settings():
    global score_information
    score_information = {}
    reset_score_info()

def reset_score_info():
    score_information['_current'] = 0

def add_score(score):
    score_information['_current'] += score

def current_score():
    return score_information['_current']

