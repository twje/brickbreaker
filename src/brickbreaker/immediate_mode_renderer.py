from .vertex_buffer_layout import VertexBufferLayout
from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .shader import Shader
import numpy as np
from OpenGL.GL import *


vertex_src = """
#version 330 core

layout(location = 0) in vec4 position;

uniform mat4 u_projTrans;

void main()
{
   gl_Position = u_projTrans * position;
};
"""

fragment_src = """
#version 330 core

layout(location = 0) out vec4 color;

void main()
{	
	color = vec4(1.0, 1.0, 1.0, 1.0);
};
"""


class ImmediateModeRenderer:
    def __init__(self, max_vertices: int, has_normals: bool, has_colors: bool, num_tex_coords: int) -> None:
        self.max_vertices = max_vertices
        self.vertex_id = 0
        self.vertices = np.zeros(max_vertices * 3, dtype=np.float32)
        self.num_vertices = 0
        self.proj_model_view = None

        # vbo
        self.vbo = VertexBuffer(self.vertices)
        self.vbo_layout = VertexBufferLayout()
        self.vbo_layout.push_float(3)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(self.vbo, self.vbo_layout)

        # shader
        self.shader = Shader(vertex_src, fragment_src)

    def begin(self, proj_model_view, primitive_type):
        self.proj_model_view = proj_model_view
        self.primitive_type = primitive_type

    def end(self):
        self.flush()

    def flush(self):
        if self.num_vertices == 0:
            return

        self.vao.bind()
        self.vbo.set_data(
            self.vertices,
            self.num_vertices * self.vbo_layout.stride
        )

        self.shader.set_uniform_mat4f("u_projTrans", self.proj_model_view)
        glDrawArrays(self.primitive_type, 0, self.num_vertices)

        self.vertex_id = 0
        self.num_vertices = 0

    def vertex(self, x: float, y: float, z: float):
        idx = self.vertex_id
        self.vertices[idx] = x
        self.vertices[idx + 1] = y
        self.vertices[idx + 2] = z

        self.vertex_id += self.vbo_layout.count
        self.num_vertices += 1

    def free_vertices_count(self):
        return self.max_vertices - self.num_vertices

    def dispose(self):
        pass
        self.vao.delete()
        self.vbo.delete()
        self.shader.delete()

