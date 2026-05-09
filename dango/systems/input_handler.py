import pygame


class InputHandler:
    # Minimal keyboard-only input mapping for MVP
    def __init__(self):
        pass

    @staticmethod
    def is_stab_pressed(events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                return True
        return False
