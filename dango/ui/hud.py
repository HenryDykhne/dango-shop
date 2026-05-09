import pygame


class HUD:
    def __init__(self, scene):
        self.scene = scene
        self.font = pygame.font.SysFont("arial", 20)

    def draw(self, screen):
        day_text = self.font.render(f"Day {self.scene.day}", True, (255, 220, 180))
        screen.blit(day_text, (20, 20))

        items_text = self.font.render(f"Balls: {len(self.scene.balls)}", True, (220, 220, 220))
        screen.blit(items_text, (20, 50))
