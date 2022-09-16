from .primitive import Rectangle
from .primitive import Circle
from .primitive import Line
from .primitive import Segment
from .primitive import OrientedRectangle
from .primitive import Point

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
    def points_collide(a: Point, b: Point) -> bool:
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
    def circle_point_collide(a: Circle, b: Point) -> bool:
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
    def rectangle_point_collide(r: Rectangle, p: Point) -> bool:
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
    def point_line(p: Point, l: Line) -> bool:
        raise NotImplemented()

    @staticmethod
    def point_segment_collide(p: Point, s: Segment) -> bool:
        raise NotImplemented()

    @staticmethod
    def point_oriented_rectangle_collide(p: Point, o_rect: OrientedRectangle) -> bool:
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
