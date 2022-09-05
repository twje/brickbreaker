from brickbreaker.core.rectangle import Rectangle
from pyrr import Vector3


def get_bottom_left(rect: Rectangle):
    return Vector3([rect.x, rect.y, 0])


def get_bottom_right(rect: Rectangle):
    return Vector3([rect.x + rect.width, rect.y, 0])


def get_top_left(rect: Rectangle):
    return Vector3([rect.x, rect.y + rect.height, 0])


def get_top_right(rect: Rectangle):
    return Vector3([rect.x + rect.width, rect.y + rect.height, 0])
