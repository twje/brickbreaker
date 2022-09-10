from dataclasses import dataclass
from pyrr import Vector3


__all__ = [
    "Line",
    "Segment",
    "Circle",
    "Rectangle",
    "OrientedRectangle"
]


@dataclass
class Line:
    base: Vector3 = Vector3()
    direction: Vector3 = Vector3()


@dataclass
class Segment:
    point1: Vector3 = Vector3()
    point2: Vector3 = Vector3()


@dataclass
class Circle:
    center: Vector3 = Vector3()
    radius: float = 0


@dataclass
class Rectangle:
    origin: Vector3 = Vector3()
    size: Vector3 = Vector3()


@dataclass
class OrientedRectangle:
    center: Vector3 = Vector3()
    half_extend: Vector3 = Vector3()
    rotation: float = 0
