import math
from brickbreaker.core.polygon import Polygon
from . import shape_utils


class EntityBase:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.bounds = Polygon()
        self._x = x
        self._y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.update_bounds()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.update_bounds()

    @property
    def speed(self):
        return math.sqrt(math.pow(self.velocity_x, 2) + math.pow(self.velocity_y, 2))

    def post_init(self):
        self.update_bounds()

    def set_velocity_by_angled(self, angle: float, value: float):
        angle = math.degrees(angle)
        self.velocity_x = value * math.cos(angle)
        self.velocity_y = value * math.sin(angle)

    def update(self, delta: float):
        new_x = self.x + self.velocity_x * delta
        new_y = self.y + self.velocity_y * delta
        self.set_position(new_x, new_y)

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y
        self.update_bounds()

    def update_bounds(self):
        self.bounds.set_position(self.x, self.y)
        self.bounds.set_vertices(self.create_vertices())

    def create_vertices(self):
        return shape_utils.create_rect(self.width, self.height)

    def is_not_active(self):
        epsilon = 1/1000
        return abs(self.velocity_x) + abs(self.velocity_y) < epsilon

    def stop(self):
        self.velocity_x = 0
        self.velocity_y = 0
