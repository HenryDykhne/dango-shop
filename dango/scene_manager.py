import pygame


class SceneManager:
    def __init__(self):
        self.current = None
        self.scene_switch_time = None

    def switch(self, new_scene):
        self.current = new_scene
        self.scene_switch_time = pygame.time.get_ticks() / 1000.0