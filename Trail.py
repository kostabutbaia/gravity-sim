class Trail:
    def __init__(self, amount: int):
        self.amount = amount
        self.points_x = []
        self.points_y = []

    def update_trail(self, point_x, point_y):
        if len(self.points_x) >= self.amount or len(self.points_y) >= self.amount:
            self.points_x = self.points_x[1:] + [point_x]
            self.points_y = self.points_y[1:] + [point_y]
        else:
            self.points_x.append(point_x)
            self.points_y.append(point_y)
        return self.get_trail()

    def get_trail(self) -> list[float]:
        return self.points_x, self.points_y