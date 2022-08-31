import math


def create_octagon(pos_x: float, pos_y: float, origin_x: float, origin_y: float, radius: float, vertex_count: float):
    vertices = []
    for index in range(0, vertex_count):
        x = origin_x + radius * \
            math.cos(math.radians(360 * index/vertex_count))
        y = origin_y + radius * \
            math.sin(math.radians(360 * index/vertex_count))
        vertices.extend([x, y])

    return vertices
