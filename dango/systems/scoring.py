class Scoring:
    def __init__(self, initial_yen=0):
        self.yen = initial_yen

    def calculate_serve(self, stick_balls):
        """Return yen value for a served stick.

        Formula: (sum of ball base values) + (10¥ × #balls ^ 2)
        stick_balls: iterable of Ball-like objects with `.value` attribute
        """
        n = len(stick_balls)
        if n == 0:
            return 0
        base = sum(getattr(b, "value", 0) for b in stick_balls)
        bonus = 10 * (n ** 2)
        return base + bonus

    def apply_serve(self, stick_balls):
        amount = self.calculate_serve(stick_balls)
        self.yen += amount
        return amount

    def apply_penalty(self, amount):
        self.yen -= amount
        return amount

    def get_yen(self):
        return self.yen
