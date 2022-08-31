import math


def create_octagon(origin_x: float, origin_y: float, radius: float, vertex_count: float):
    vertices = []
    for index in range(0, vertex_count):
        x = origin_x + radius * \
            math.cos(math.radians(360 * index/vertex_count))
        y = origin_y + radius * \
            math.sin(math.radians(360 * index/vertex_count))
        vertices.extend([x, y])

    return vertices


def create_rect(x: float, y: float, width: float, height: float):
    return [
        x, y,
        x + width, y,
        x + width, y + height,
        x, y + height
    ]
