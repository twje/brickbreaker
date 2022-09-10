from .primitive import Rectangle
from .primitive import Circle
from .primitive import Line
from .primitive import Segment
from .primitive import OrientedRectangle
from pyrr import Vector3

__all__ = ["Intersector"]


class Intersector:
    # -----------------------------
    # Homogeneous Collission Checks
    # -----------------------------
    @staticmethod
    def rectangles_collide(a: Rectangle, b: Rectangle) -> bool:
        raise NotImplemented()

    @staticmethod
    def circles_collide(a: Circle, b: Circle) -> bool:
        raise NotImplemented()

    @staticmethod
    def points_collide(a: Vector3, b: Vector3) -> bool:
        raise NotImplemented()

    @staticmethod
    def lines_collide(a: Line, b: Line) -> bool:
        raise NotImplemented()

    @staticmethod
    def segments_collide(a: Segment, b: Segment) -> bool:
        raise NotImplemented()

    @staticmethod
    def oriented_rectangle_collide(a: OrientedRectangle, b: OrientedRectangle) -> bool:
        raise NotImplemented()

    # -------------------------------
    # Heterogeneous Collission Checks
    # -------------------------------
    @staticmethod
    def circle_point_collide(a: Circle, b: Vector3) -> bool:
        raise NotImplemented()

    @staticmethod
    def circle_line_collide(a: Circle, b: Line) -> bool:
        raise NotImplemented()

    @staticmethod
    def circle_segment_collide(a: Circle, b: Segment) -> bool:
        raise NotImplemented()

    @staticmethod
    def circle_rectangle_collide(a: Circle, b: Rectangle) -> bool:
        raise NotImplemented()

    @staticmethod
    def circle_oriented_rectangle_collide(a: Circle, b: Rectangle) -> bool:
        raise NotImplemented()

    @staticmethod
    def rectangle_point_collide(r: Rectangle, p: Vector3) -> bool:
        raise NotImplemented()

    @staticmethod
    def rectangle_line_collide(r: Rectangle, l: Line) -> bool:
        raise NotImplemented()

    @staticmethod
    def rectangle_segment_collide(r: Rectangle, s: Segment) -> bool:
        raise NotImplemented()

    @staticmethod
    def rectangle_oriented_rectangle_collide(rect: Rectangle, o_rect: OrientedRectangle) -> bool:
        raise NotImplemented()

    @staticmethod
    def point_line(p: Vector3, l: Line) -> bool:
        raise NotImplemented()

    @staticmethod
    def point_segment_collide(p: Vector3, s: Segment) -> bool:
        raise NotImplemented()

    @staticmethod
    def point_oriented_rectangle_collide(p: Vector3, o_rect: OrientedRectangle) -> bool:
        raise NotImplemented()

    @staticmethod
    def line_line_segment_collide(line: Line, segment: Segment) -> bool:
        raise NotImplemented()

    @staticmethod
    def line_oriented_rectangle_collide(line: Line, o_rect: OrientedRectangle) -> bool:
        raise NotImplemented()

    @staticmethod
    def segment_oriented_rectangle_collide(segment: Segment, o_rect: OrientedRectangle) -> bool:
        raise NotImplemented()


# --------------
# Helper Methods
# --------------


# import math
# import sys

# from brickbreaker.core.circle import Circle
# from brickbreaker.core.rectangle import Rectangle
# from .polygon import Polygon
# from pyrr import Vector3


# class Intersector:
#     tmp: Vector3 = Vector3()
#     tmp1: Vector3 = Vector3()
#     tmp2: Vector3 = Vector3()
#     tmp3: Vector3 = Vector3()

#     @staticmethod
#     def circle_rectangle_collide(circle: Circle, rect: Rectangle) -> bool:
#         pass

#     @staticmethod
#     def clamp_on_rectangle(x: float, y: float, rect: Rectangle) -> bool:
#         pass

#     @classmethod
#     def intersect_segment_circle(cls, start: Vector3, end: Vector3, center: Vector3, radius_squared: float) -> bool:
#         cls.tmp.xy = [end.x - start.x, end.y - start.y]
#         cls.tmp1.xy = [center.x - start.x, center.y - start.y]

#         l = cls.tmp.length
#         cls.tmp.normalize()
#         u = cls.tmp1.dot(cls.tmp)

#         if u <= 0:
#             cls.tmp2.xy = [start.x, start.y]
#         elif u >= l:
#             cls.tmp2.xy = [end.x, end.y]
#         else:
#             cls.tmp3 = cls.tmp * u
#             cls.tmp2.xy = [cls.tmp3.x + start.x, cls.tmp3.y + start.y]

#         x = center.x - cls.tmp2.x
#         y = center.y - cls.tmp2.y

#         return x * x + y * y <= radius_squared

#     @classmethod
#     def overlap_convex_polygons(cls, polygon1: Polygon, polygon2: Polygon) -> bool:
#         overlap = cls.overlap_convex_polygons_alg(polygon1, polygon2)
#         if overlap:
#             overlap = cls.overlap_convex_polygons_alg(polygon2, polygon1)
#         return overlap

#     @classmethod
#     def overlap_convex_polygons_alg(cls, polygon1: Polygon, polygon2: Polygon) -> bool:
#         """SAT theorem."""
#         verts1 = polygon1.get_transformed_vertices()
#         verts2 = polygon2.get_transformed_vertices()

#         for index in range(0, len(verts1), 2):
#             axis_x, axis_y = cls.compute_normal_from_segment(verts1, index)

#             min_a, max_a = cls.compute_min_max_of_projection(
#                 verts1, axis_x, axis_y)
#             min_b, max_b = cls.compute_min_max_of_projection(
#                 verts2, axis_x, axis_y)

#             if max_a < min_b or max_b < min_a:
#                 return False

#         return True

#     @staticmethod
#     def compute_normal_from_segment(verts, index):
#         # segment
#         length = len(verts)
#         x1 = verts[index]
#         y1 = verts[index + 1]
#         x2 = verts[(index + 2) % length]
#         y2 = verts[(index + 3) % length]

#         # axis is negative reciprocal of segment slope (counter clockwise) - 90 degrees
#         # proof - https://www.youtube.com/watch?v=HyThzLRuqXo
#         axis_x = y1 - y2
#         axis_y = -(x1 - x2)

#         # normalize axis
#         length = math.sqrt(axis_x * axis_x + axis_y * axis_y)
#         axis_x /= length
#         axis_y /= length

#         return axis_x, axis_y

#     @staticmethod
#     def compute_min_max_of_projection(verts, axis_x, axis_y):
#         min_a = sys.float_info.max
#         max_a = sys.float_info.min
#         for v in range(0, len(verts), 2):
#             p = verts[v] * axis_x + verts[v + 1] * axis_y
#             min_a = min(min_a, p)
#             max_a = max(max_a, p)

#         return min_a, max_a
