import pygame
from dango.settings import BALL_COLORS, FIELD_TOP


class HUD:
    def __init__(self, scene):
        self.scene = scene
        self.font = pygame.font.SysFont("arial", 20)

    def draw(self, screen):
        day_text = self.font.render(f"Day {self.scene.day}", True, (255, 220, 180))
        screen.blit(day_text, (20, 20))

        items_text = self.font.render(f"Balls: {len(self.scene.balls)}", True, (220, 220, 220))
        screen.blit(items_text, (20, 50))

        # draw upcoming queue (if available)
        if hasattr(self.scene, 'queue'):
            items = self.scene.queue.as_list()
            # position the queue in the top UI row (next to Day / Balls)
            base_x = 260
            base_y = 50
            radius = 12
            spacing = 8

            label = self.font.render("Queue:", True, (255, 220, 180))
            screen.blit(label, (base_x, base_y - 30))

            for i, key in enumerate(items):
                color = BALL_COLORS.get(key, (120, 120, 120))
                x = base_x + i * (radius * 2 + spacing) + radius
                pygame.draw.circle(screen, color, (int(x), int(base_y)), radius)
                pygame.draw.circle(screen, (0, 0, 0), (int(x), int(base_y)), radius, 2)

            # front-of-queue indicator above the first item
            if items:
                front_x = base_x + radius
                top_y = base_y - radius - 8
                left_x = front_x - 8
                right_x = front_x + 8
                tri_points = [(int(front_x), int(top_y)), (int(left_x), int(base_y - radius + 6)), (int(right_x), int(base_y - radius + 6))]
                pygame.draw.polygon(screen, (255, 255, 255), tri_points)
                pygame.draw.polygon(screen, (0, 0, 0), tri_points, 1)
                screen.blit(label, (int(front_x - label.get_width() / 2), int(top_y - label.get_height() - 2)))
