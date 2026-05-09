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
        # visual indicator for a recent parry-up: dict with t,dur,slot
        self.parry_indicator = None

    def handle_events(self, events, manager):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from dango.scenes.level_select import LevelSelect
                    manager.switch(LevelSelect())
                if event.key == pygame.K_SPACE:
                    # stab action: visual + collision using stab hitbox
                    self.player.start_stab()
                    self.player.stab(self.balls)
                if event.key == pygame.K_h:
                    # parry up: jump colliding ball to second place in the queue
                    # compute parry hitbox at t=0 and use it for collision
                    parry_rect = self.player.compute_parry_rect('up', prog=0.0)
                    had_parry = False
                    for b in list(self.balls):
                        if b.alive and parry_rect.colliderect(b.get_rect()):
                            # insert into second position (index 1)
                            self.queue.insert_at(1, getattr(b, 'color_key', None))
                            b.alive = False
                            had_parry = True
                            break
                    # visual parry and indicator if successful
                    if had_parry:
                        self.player.start_parry('up')
                        self.parry_indicator = {'t': 0.0, 'dur': 0.8, 'slot': 1}
                if event.key == pygame.K_j:
                    # parry down: send colliding ball back to the hopper bag
                    parry_rect = self.player.compute_parry_rect('down', prog=0.0)
                    for b in list(self.balls):
                        if b.alive and parry_rect.colliderect(b.get_rect()):
                            self.bag.add(getattr(b, 'color_key', None))
                            b.alive = False
                    # visual parry
                    self.player.start_parry('down')

    def update(self, dt, manager):
        self.player.update(dt)
        # advance parry indicator timer
        if self.parry_indicator is not None:
            self.parry_indicator['t'] += dt
            if self.parry_indicator['t'] >= self.parry_indicator['dur']:
                self.parry_indicator = None
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
