from dataclasses import dataclass
from OpenGL.GL import *


@dataclass
class VertexBufferElement:
    name: str
    type: int
    count: int
    normalized: False

    @staticmethod
    def get_size_of_type(type: int) -> int:
        if type == GL_FLOAT:
            return 4
        elif type == GL_UNSIGNED_INT:
            return 4
        elif type == GL_UNSIGNED_BYTE:
            return 1


class VertexBufferLayout:
    def __init__(self) -> None:
        self.elements: VertexBufferElement = []
        self.stride = 0
        self.count = 0

    def push_float(self, count: int, name: str = None) -> None:
        self.push(count, GL_FLOAT, name)

    def push_int(self, count: int, name: str = None) -> None:
        self.push(count, GL_UNSIGNED_INT, name)

    def push_char(self, count: int, name: str = None) -> None:
        self.push(count, GL_UNSIGNED_BYTE, name)

    def push(self, count: int, type: int, name: str):
        element = VertexBufferElement(name, type, count, GL_FALSE)
        self.elements.append(element)
        self.stride += VertexBufferElement.get_size_of_type(type) * count
        self.count += count
