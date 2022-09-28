from .vertex_buffer_layout import VertexBufferLayout
import numpy as np

__all__ = ["Geometry"]


class Geometry:
    def __init__(self) -> None:
        self.element_lookup = {}
        self.elements = []
        self.layout = VertexBufferLayout()
        self.index = 0
        self.has_data = False
        self.vertices = None

    @property
    def vertex_count(self):
        return self.index

    @property
    def size(self):
        return self.vertex_count * self.layout.stride

    def push_element(self, name: str, count: int, layout_id: str = None):
        self.element_lookup[name] = len(self.elements)
        self.elements.append((self.layout.count, layout_id))
        self.layout.push_float(count, layout_id)

    def finalize(self, max_vertices: int):
        self.vertices = np.zeros(
            max_vertices * self.layout.count,
            dtype=np.float32
        )

    def push_data(self, name: str, data: list):
        assert len(data) > 0

        if name not in self.element_lookup:
            return

        count, _ = self.elements[self.element_lookup[name]]
        for index, item in enumerate(data):
            offset = self.index * self.layout.count + count
            self.vertices[offset + index] = item
        self.has_data = True

    def next(self):
        self.index += 1

    def reset(self):
        self.index = 0
        self.has_data = False
