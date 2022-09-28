from dataclasses import dataclass
from typing import Tuple
from pyrr import Vector3


__all__ = [
    "Line",
    "Segment",
    "Circle",
    "Rectangle",
    "OrientedRectangle",
    "Point"
]

# Type Aliases
VectorTuple2D = Tuple[float, float]


# ----------------
# Helper Functions
# ----------------
def is_zero_vector(value: Vector3) -> bool:
    freshhold = 1/10000
    return abs(value.x) + abs(value.y) <= freshhold


# -----------------
# Class Definitions
# -----------------
@dataclass
class Line:
    base: Vector3 = Vector3()
    direction: Vector3 = Vector3()

    def __init__(self, base: VectorTuple2D = (0, 0), direction: VectorTuple2D = (0, 0)) -> None:
        self.base.xy = base
        self.direction = Vector3([direction[0], direction[1], 0])


@dataclass
class Segment:
    point1: Vector3 = Vector3()
    point2: Vector3 = Vector3()

    def __init__(self, point1: VectorTuple2D = (0, 0), point2: VectorTuple2D = (0, 0)) -> None:
        self.point1 = Vector3([point1[0], point1[1], 0])
        self.point2 = Vector3([point2[0], point2[1], 0])


@dataclass
class Circle:
    _center: Vector3 = Vector3()
    _radius: float = 0
    _dirty: float = True

    def __init__(self, center: VectorTuple2D = (0, 0), radius: float = 0) -> None:
        self.center = Vector3([center[0], center[1], 0])
        self.radius = radius


@dataclass
class Rectangle:
    origin: Vector3 = Vector3()
    size: Vector3 = Vector3()

    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.origin = Vector3([x, y, 0])
        self.size = Vector3([width, height, 0])

    @property
    def x(self):
        return self.origin.x

    @x.setter
    def x(self, value: float):
        self.origin.x = value

    @property
    def y(self):
        return self.origin.x

    @y.setter
    def y(self, value: float):
        self.origin.y = value

    @property
    def width(self):
        return self.size.x

    @width.setter
    def width(self, value: float):
        self.size.x = value

    @property
    def height(self):
        return self.size.y

    @height.setter
    def height(self, value: float):
        self.size.y = value


@dataclass
class OrientedRectangle:
    center: Vector3 = Vector3()
    half_extend: Vector3 = Vector3()
    rotation: float = 0

    def __init__(self, center: VectorTuple2D = (0, 0), half_extend: float = 0, rotation: float = 0) -> None:
        self.center = Vector3([center[0], center[1], 0])
        self.half_extend = Vector3([half_extend[0], half_extend[1], 0])
        self.rotation = rotation


Point = Vector3
