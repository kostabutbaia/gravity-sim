class Object:
    def __init__(self, m: float, r: list[float], v: list[float]):
        self.m = m
        self.r = r
        self.v = v
        self._prev_r = None
        self._initialized = False