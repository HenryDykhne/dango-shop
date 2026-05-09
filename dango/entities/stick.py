class Stick:
    def __init__(self, max_balls):
        self.max_balls = max_balls
        self.balls = []

    def add(self, ball):
        if len(self.balls) < self.max_balls:
            self.balls.append(ball)
            return True
        return False
        
    def clear(self):
        self.balls.clear()
