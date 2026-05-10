import pygame
from dango.settings import BALL_COLORS, DAYS, current_score


class HUD:
    def __init__(self, scene):
        self.scene = scene
        self.font = pygame.font.SysFont("arial", 20)

    def draw(self, screen):
        day_text = self.font.render(f"Day {self.scene.day}", True, (255, 220, 180))
        screen.blit(day_text, (20, 15))
        score = current_score()
        items_text = self.font.render(f"Quota: ¥{score}/¥{DAYS[self.scene.day-1]['quota']}", True, (220, 220, 220))
        screen.blit(items_text, (20, 45))
        time_text = self.font.render(f"End of Day in: {int(self.scene.time_remaining)}s", True, (220, 220, 220))
        screen.blit(time_text, (20, 75))

        # draw upcoming queue (if available)
        if hasattr(self.scene, 'queue'):
            items = self.scene.queue.as_list()
            # position the queue in the top UI row (next to Day / Balls)
            base_x = 260
            base_y = 60
            radius = 12
            spacing = 8

            label = self.font.render("Queue:", True, (255, 220, 180))
            #screen.blit(label, (base_x, base_y - 30))

            for i, key in enumerate(items):
                color = BALL_COLORS.get(key, (120, 120, 120))
                x = base_x + i * (radius * 2 + spacing) + radius
                pygame.draw.circle(screen, color, (int(x), int(base_y)), radius)
                pygame.draw.circle(screen, (0, 0, 0), (int(x), int(base_y)), radius, 2)

            # front-of-queue indicator: triangle pointing down, above the first item
            if items:
                front_x = base_x + radius
                # apex (point) of triangle is below the base of the triangle
                apex_y = base_y - radius + 6
                left_x = front_x - 8
                right_x = front_x + 8
                top_y_tri = base_y - radius - 8
                # triangle points downwards (apex closer to the circle)
                tri_points = [
                    (int(left_x), int(top_y_tri)),
                    (int(right_x), int(top_y_tri)),
                    (int(front_x), int(apex_y)),
                ]
                pygame.draw.polygon(screen, (255, 255, 255), tri_points)
                pygame.draw.polygon(screen, (0, 0, 0), tri_points, 1)
                # place label above the triangle
                label = self.font.render("Front", True, (255, 255, 255))
                label_y = top_y_tri - label.get_height() - 4
                screen.blit(label, (int(front_x - label.get_width() / 2), int(label_y)))

            # parry-up indicator: blinking red triangle above the slot a ball was parried into
            pi = getattr(self.scene, 'parry_indicator', None)
            if pi and items and 0 <= pi.get('slot', 0) < len(items):
                # blink on/off
                visible = int(pi['t'] * 6) % 2 == 0
                if visible:
                    slot = pi['slot']
                    px = base_x + slot * (radius * 2 + spacing) + radius
                    apex_y = base_y - radius + 6
                    left_x = px - 8
                    right_x = px + 8
                    top_y_tri = base_y - radius - 8
                    tri_points = [
                        (int(left_x), int(top_y_tri)),
                        (int(right_x), int(top_y_tri)),
                        (int(px), int(apex_y)),
                    ]
                    pygame.draw.polygon(screen, (220, 40, 40), tri_points)
                    pygame.draw.polygon(screen, (0, 0, 0), tri_points, 1)
