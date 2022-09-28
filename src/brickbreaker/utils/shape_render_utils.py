from brickbreaker.core.polygon import Polygon
from brickbreaker.core.shape_renderer import ShapeRenderer
from brickbreaker.core.primitive import Line
from brickbreaker.core.primitive import Rectangle
from brickbreaker.core.primitive import OrientedRectangle
from brickbreaker.core.primitive import Segment
from brickbreaker.core.primitive import Circle
from . import shape_utils

__all__ = [
    "line",
    "segment",
    "circle",
    "rectangle",
    "oriented_rectangle"
]


def line(renderer: ShapeRenderer, line: Line, magnitude: float = 10000) -> None:
    x1, y1 = line.base.xy
    x2, y2 = (line.base + line.direction * magnitude).xy
    renderer.line(x1, y1, x2, y2)


def segment(renderer: ShapeRenderer, segment: Segment) -> None:
    x1, y1 = segment.point1.xy
    x2, y2 = segment.point2.xy
    renderer.line(x1, y1, x2, y2)


def circle(renderer: ShapeRenderer, circle: Circle, vertex_count=8):
    vertices = shape_utils.create_octagon(
        circle.center.x,
        circle.center.y,
        circle.radius,
        vertex_count
    )
    renderer.polygon(vertices)


def rectangle(renderer: ShapeRenderer, rect: Rectangle):
    renderer.rect(*rect.origin.xy, *rect.size.xy)


def oriented_rectangle(renderer: ShapeRenderer, o_rect: OrientedRectangle):
    tl = shape_utils.oriented_rectangle_corner(o_rect, shape_utils.Corner.TL)
    tr = shape_utils.oriented_rectangle_corner(o_rect, shape_utils.Corner.TR)
    br = shape_utils.oriented_rectangle_corner(o_rect, shape_utils.Corner.BR)
    bl = shape_utils.oriented_rectangle_corner(o_rect, shape_utils.Corner.BL)
    renderer.polygon([tl.x, tl.y, tr.x, tr.y, br.x, br.y, bl.x, bl.y])


def polygon(renderer: ShapeRenderer, polygon: Polygon):
    renderer.polygon(polygon.get_transformed_vertices())
