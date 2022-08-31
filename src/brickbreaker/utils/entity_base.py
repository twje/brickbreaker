from brickbreaker.core.polygon import Polygon


class EntityBase:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.bounds = Polygon()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def post_init(self):
        self.bounds = Polygon()
        self.bounds.set_vertices(self.create_vertices())

    def update(self, delta: float):
        pass
