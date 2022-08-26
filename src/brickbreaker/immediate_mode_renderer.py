from .vertex_buffer_layout import VertexBufferLayout
from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .shader import Shader
import numpy as np
from OpenGL.GL import *


vertex_src = """
#version 330 core

layout(location = 0) in vec4 a_position;
layout(location = 1) in vec4 a_color;

out vec4 v_color;

uniform mat4 u_projTrans;

void main()
{
   gl_Position = u_projTrans * a_position;
   v_color = a_color;
};
"""

fragment_src = """
#version 330 core

out vec4 out_color;
in vec4 v_color;

void main()
{	
	// out_color = vec4(1.0, 1.0, 1.0, 1.0);
    out_color = v_color;
};
"""


class ImmediateModeRenderer:
    def __init__(self, max_vertices: int, has_normals: bool, has_colors: bool, num_tex_coords: int) -> None:
        self.max_vertices = max_vertices
        self.vertex_id = 0
        self.vertices = np.zeros(max_vertices * 3, dtype=np.float32)
        self.num_vertices = 0
        self.proj_model_view = None

        # shader
        self.shader = Shader(vertex_src, fragment_src)

        # vbo
        self.vbo = VertexBuffer(self.vertices)
        self.vbo_layout = VertexBufferLayout()
        self.vbo_layout.push_float(3, "a_position")
        self.vbo_layout.push_float(4, "a_color")

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(self.vbo, self.vbo_layout, self.shader)

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
        self.vertices[idx + 3] = 1
        self.vertices[idx + 4] = 1
        self.vertices[idx + 5] = 1
        self.vertices[idx + 6] = 1

        self.vertex_id += self.vbo_layout.count
        self.num_vertices += 1

    def free_vertices_count(self):
        return self.max_vertices - self.num_vertices

    def dispose(self):
        pass
        self.vao.delete()
        self.vbo.delete()
        self.shader.delete()
