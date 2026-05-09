import pygame
from dango.entities.player import Player
from dango.entities.cannon import Cannon
from dango.entities.Customers import Customers
from dango.systems.bag import Bag, Queue
from dango.settings import DAYS
from dango.ui.hud import HUD


class GameScene:
    def __init__(self, day=1):
        self.day = day
        cfg = DAYS[day-1]
        self.bag = Bag(cfg["bag"])
        # the cannon will feed from this queue; it is prefilled from the bag
        self.queue = Queue(self.bag, size=8)
        self.player = Player(200, 400)
        self.cannon = Cannon()
        self.balls = []
        self.volley_gap = cfg.get("volley_gap", 3.0)
        self.font = pygame.font.SysFont("arial", 24)
        self.customers = Customers(self.day)
        self.hud = HUD(self)

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from dango.scenes.level_select import LevelSelect
                    manager.switch(LevelSelect())
                if event.key == pygame.K_SPACE:
                    # stab action
                    self.player.stab(self.balls)
                if event.key == pygame.K_h:
                    # parry up: jump colliding ball to second place in the queue
                    for b in list(self.balls):
                        if b.alive and self.player.rect.colliderect(b.get_rect()):
                            # insert into second position (index 1)
                            self.queue.insert_at(1, getattr(b, 'color_key', None))
                            b.alive = False
                if event.key == pygame.K_j:
                    # parry down: send colliding ball back to the hopper bag
                    for b in list(self.balls):
                        if b.alive and self.player.rect.colliderect(b.get_rect()):
                            self.bag.add(getattr(b, 'color_key', None))
                            b.alive = False

    def update(self, dt, manager):
        self.player.update(dt)
        # update cannon (it will decide when to fire based on its own timer)
        spawned = self.cannon.update(dt, self.queue, self.volley_gap)
        if spawned:
            self.balls.extend(spawned)

        for b in list(self.balls):
            b.update(dt)
            if not b.alive:
                try:
                    self.balls.remove(b)
                except ValueError:
                    pass

        self.customers.update(dt)

    def draw(self, screen):
        # draw field background
        pygame.draw.rect(screen, (60, 40, 20), (0, 80, 1280, 560))

        for b in self.balls:
            b.draw(screen)

        self.player.draw(screen)
        self.cannon.draw(screen)
        self.customers.draw(screen)

        self.hud.draw(screen)
