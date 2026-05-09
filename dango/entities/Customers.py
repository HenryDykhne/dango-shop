import math
import pygame
import random
from dango.settings import DAYS


class Customer:
    ENTERING = 1
    WAITING = 2
    LEAVING = 3
    GONE = 4

    TIMINGS = {
        ENTERING: 1,
        WAITING: 10,
        LEAVING: 1,
        GONE: 1e100,
    }

    def __init__(self, day, xOffset):
        self.age = 0.0
        self.phase = Customer.ENTERING
        self.xOffset = xOffset
        self.y = 0.0
        self.red = 0
        self.alpha = 0
        self.radius = 32

        # generate what the customer wants
        self.demand = []
        day_config = DAYS[day]
        for _ in range(day_config['stick_size']):
            options = list(day_config['bag'].values())
            while (thing := random.choice(options)) in ['wasabi', 'coal']:
                pass
            self.demand.append(random.choice(options))

    def offer(self, stick):
        if self.phase == Customer.WAITING and stick == self.demand:
            self.age = 0.0
            self.phase = Customer.self.LEAVING
            return True
        return False

    def isGone(self):
        return self.phase == Customer.GONE

    def update(self, dt):
        ratio = min(1, self.age / Customer.TIMINGS[self.phase])
        self.age += dt
        if self.age > Customer.TIMINGS[self.phase]:
            self.age = 0
            self.phase += 1

        if self.phase == Customer.ENTERING:
            self.y = 720 - 180 * ratio
            self.alpha = int(255 * ratio)
            self.red = 0
        elif self.phase == Customer.WAITING:
            self.y = 720 - 180
            self.alpha = 255
            self.red = int(255 * ratio)
        elif self.phase == Customer.LEAVING:
            self.y = 720 - 180*(1-ratio)
            self.alpha = int(255*(1 - ratio))
        else:
            self.y = 720
            self.alpha = 0


    def draw(self, screen):
        if self.phase != Customer.GONE:
            color = (255, 255 - self.red, 255 - self.red, self.alpha)
            pygame.draw.circle(screen, color, (int(self.xOffset), int(self.y)), self.radius)


class Customers:
    MAX_CUSTOMERS = 8
    COOLDOWNS = [2] #[12, 32, 14, 10, 25, 24]

    def __init__(self, day):
        self.stalls = [None]*Customers.MAX_CUSTOMERS
        self._reset_cooldown()
        self.free_stalls = list(range(Customers.MAX_CUSTOMERS))
        self.day = day

    def _reset_cooldown(self):
        self.cooldown = random.choice(Customers.COOLDOWNS)

    def offer(stick):
        for customer in self.stalls:
            if customer != None and customer.offer(stick):
                return True
        return False

    def update(self, dt):
        self.cooldown -= dt

        # add new customers
        if self.cooldown <= 0 and self.free_stalls:
            random.shuffle(self.free_stalls)
            i = self.free_stalls.pop()

            offset = int(1080*( (i + 1) / (Customers.MAX_CUSTOMERS + 2) ))
            self.stalls[i] = Customer(self.day, offset)

            self._reset_cooldown()
        
        # Update the individual customers and remove them if they are gone
        for i in range(Customers.MAX_CUSTOMERS):
            customer = self.stalls[i]
            if customer != None:
                customer.update(dt)
                if customer.isGone():
                    self.stalls[i] = None
                    self.free_stalls.append(i)
        
        print(self.cooldown, self.stalls)

    def draw(self, screen):
        for i in range(Customers.MAX_CUSTOMERS):
            customer = self.stalls[i]
            if customer != None:
                customer.draw(screen)

    