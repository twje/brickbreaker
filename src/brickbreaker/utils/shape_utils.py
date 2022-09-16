from enum import Enum
from enum import auto
import math
from brickbreaker.core.primitive import OrientedRectangle
from pyrr import Vector3
import pyrr


class Corner(Enum):
    TL = auto()
    TR = auto()
    BL = auto()
    BR = auto()


def create_octagon(origin_x: float, origin_y: float, radius: float, vertex_count: float):
    vertices = []
    for index in range(0, vertex_count):
        x = origin_x + radius * \
            math.cos(math.radians(360 * index/vertex_count))
        y = origin_y + radius * \
            math.sin(math.radians(360 * index/vertex_count))
        vertices.extend([x, y])

    return vertices


def create_rect(width: float, height: float):
    return [
        0, 0,
        width, 0,
        width, height,
        0,  height
    ]


def rotate_vector(vector: Vector3, angle: float) -> Vector3:
    rotate_matrix = pyrr.matrix33.create_from_z_rotation(math.radians(angle))
    return pyrr.matrix33.multiply(vector, rotate_matrix)


def oriented_rectangle_corner(o_rect: OrientedRectangle, corner_id: Corner) -> Vector3:
    corner = o_rect.half_extend.copy()
    if corner_id == Corner.TL:
        corner.x = -corner.x
    elif corner_id == Corner.TR:
        pass
    elif corner_id == Corner.BR:
        corner.y = -corner.y
    else:
        corner = -corner

    corner = rotate_vector(corner, o_rect.rotation)
    return corner + o_rect.center
