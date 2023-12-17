class Object:
    def __init__(self, m: float, r: list[float], v: list[float]):
        self.m = m
        self.r = r
        self.v = v
        self.prev_r = None
        self.positions = [r]
        self.velocities = [v]
        self.first_iter = True