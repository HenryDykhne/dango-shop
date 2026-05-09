import pygame

from dango.entities.player import Player
from dango.entities.cannon import Cannon
from dango.entities.Customers import Customers
from dango.entities.dangoHolders import DangoHolders
from dango.systems.bag import Bag, Queue
from dango.settings import DAYS, PARRY_ENDLAG_DURATION, STAB_ENDLAG_DURATION
from dango.ui.hud import HUD


class GameScene:
    def __init__(self, day=1):
        self.day = day
        cfg = DAYS[day-1]
        self.bag = Bag(cfg["bag"])
        # the cannon will feed from this queue; it is prefilled from the bag
        self.queue = Queue(self.bag, size=8)
        self.dango_holders = DangoHolders()
        self.player = Player(200, 400, day=day, add_stick=self.dango_holders.add_stick)
        self.cannon = Cannon()
        self.balls = []
        
        self.volley_gap = cfg.get("volley_gap", 3.0)
        self.font = pygame.font.SysFont("arial", 24)
        self.customers = Customers(self.day)
        self.hud = HUD(self)
        # visual indicator for a recent parry-up: dict with t,dur,slot
        self.parry_indicator = None
        self.last_parry_time = None
        self.last_stab_time = None

    def handle_events(self, events, manager):
        if self.player.scramble_controls_till > pygame.time.get_ticks() / 1000.0:
            parry_up_key = pygame.K_j
            parry_down_key = pygame.K_h
        else:
            parry_up_key = pygame.K_h
            parry_down_key = pygame.K_j
        current_time = pygame.time.get_ticks() / 1000
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from dango.scenes.level_select import LevelSelect
                    manager.switch(LevelSelect())
                if event.key == pygame.K_SPACE \
                    and (self.last_stab_time is None or (current_time - self.last_stab_time) > STAB_ENDLAG_DURATION):
                    self.last_stab_time = current_time
                    # stab action: visual + collision using stab hitbox
                    self.player.start_stab()
                    self.player.stab(self.balls)
                if event.key == parry_up_key \
                    and (self.last_parry_time is None or (current_time - self.last_parry_time) > PARRY_ENDLAG_DURATION):
                    self.last_parry_time = current_time
                    # parry up: jump colliding ball to second place in the queue
                    # compute parry hitbox at t=0 and use it
                    #  for collision
                    parry_rect = self.player.compute_parry_rect('up', prog=0.0)
                    had_parry = False
                    for b in list(self.balls):
                        if b.alive and parry_rect.colliderect(b.get_rect()):
                            # insert into second position (index 1)
                            self.queue.insert_at(1, getattr(b, 'color_key', None))
                            b.alive = False
                            had_parry = True
                            break
                    # always show the visual parry; indicator only on success
                    self.player.start_parry('up')
                    if had_parry:
                        self.parry_indicator = {'t': 0.0, 'dur': 0.8, 'slot': 1}
                if event.key == parry_down_key \
                    and (self.last_parry_time is None or (current_time - self.last_parry_time) > PARRY_ENDLAG_DURATION):
                    self.last_parry_time = current_time
                    # parry down: send colliding ball back to the hopper (not really back to the bag though)
                    parry_rect = self.player.compute_parry_rect('down', prog=0.0)
                    for b in list(self.balls):
                        if b.alive and parry_rect.colliderect(b.get_rect()):
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
            # pass the full player object so balls can react to player state
            b.update(dt, self.player)
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
        self.dango_holders.draw(screen)

        self.hud.draw(screen)
