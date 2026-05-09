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
