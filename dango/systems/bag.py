import random


class Bag:
    def __init__(self, counts):
        # counts: dict of color_key -> count
        self.base = counts.copy()
        self._rebuild()

    def _rebuild(self):
        self.pool = []
        for k, v in self.base.items():
            self.pool.extend([k] * v)
        random.shuffle(self.pool)

    def draw(self):
        if not self.pool:
            self._rebuild()
        return self.pool.pop()

    def add(self, color_key):
        # add a color back into the hopper; appended to pool
        self.pool.append(color_key)


class Queue:
    """A simple fixed-size queue of upcoming color keys backed by a Bag.

    The queue preloads `size` items from the bag and keeps itself filled
    as items are popped. Inserting beyond capacity returns the overflow
    to the bag.
    """
    def __init__(self, bag, size=8):
        self.bag = bag
        self.size = size
        self.items = []
        self._fill()

    def _fill(self):
        while len(self.items) < self.size:
            self.items.append(self.bag.draw())

    def pop(self):
        if not self.items:
            self._fill()
        val = self.items.pop(0)
        self._fill()
        return val

    def insert_at(self, index, color_key):
        # ignore invalid inserts
        if color_key is None:
            return

        if index < 0:
            index = 0
        if index > len(self.items):
            index = len(self.items)

        # insert and push everything after it back one slot
        self.items.insert(index, color_key)

        # if we exceeded capacity, return the last item to the bag
        if len(self.items) > self.size:
            overflow = self.items.pop()
            # don't add None back into the bag
            if overflow is not None:
                self.bag.add(overflow)

    def as_list(self):
        return list(self.items)
