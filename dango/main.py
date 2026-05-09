import sys
try:
    import pygame
except Exception:
    print("Pygame is required to run this project. Install with: pip install -r requirements.txt")
    sys.exit(1)

from dango.scene_manager import SceneManager
from dango.scenes.level_select import LevelSelect
from dango.settings import SCREEN_W, SCREEN_H, FPS, init_settings


def run():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Dango Shop - Prototype")
    clock = pygame.time.Clock()

    manager = SceneManager()
    manager.switch(LevelSelect())

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.current.handle_events(events, manager)
        manager.current.update(dt, manager)

        screen.fill((30, 30, 30))
        manager.current.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    init_settings()
    run()
