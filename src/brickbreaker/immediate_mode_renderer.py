from .vertex_buffer_layout import VertexBufferLayout
from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .shader import Shader
import numpy as np
from OpenGL.GL import *


class ImmediateModeRenderer:
    def __init__(self, max_vertices: int, has_normals: bool, has_colors: bool, num_tex_coords: int) -> None:
        self.has_colors = has_colors
        self.max_vertices = max_vertices
        self.vertex_id = 0
        self.vertices = np.zeros(max_vertices * 3, dtype=np.float32)
        self.num_vertices = 0
        self.proj_model_view = None
        self.color_offset = 0

        # shader
        self.shader = Shader(
            self.create_vertex_shader(has_colors),
            self.create_fragment_shader(has_colors)
        )

        # vbo
        self.vbo = VertexBuffer(self.vertices)
        self.vbo_layout = VertexBufferLayout()
        self.vbo_layout.push_float(3, "a_position")

        if has_colors:
            self.color_offset = self.vbo_layout.count
            self.vbo_layout.push_float(4, "a_color")

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(self.vbo, self.vbo_layout, self.shader)

    def create_vertex_shader(self, has_colors):
        color_attribute = "in vec4 a_color;" if has_colors else ""
        color_out = "out vec4 v_color;" if has_colors else ""
        color_assign = "v_color = a_color;" if has_colors else ""

        return """
            #version 330 core
            in vec4 a_position;
            {color_attribute}
            {color_out}
            uniform mat4 u_projTrans;
            void main()
            {{
                gl_Position = u_projTrans * a_position;
                {color_assign}
            }}
        """.format(
            color_attribute=color_attribute,
            color_out=color_out,
            color_assign=color_assign
        )

    def create_fragment_shader(self, has_colors):
        color_in = "in vec4 v_color;" if has_colors else ""
        color_assign = "v_color;" if has_colors else "vec4(1.0, 1.0, 1.0, 1.0);"

        return """
            #version 330 core
            out vec4 out_color;
            {color_in}
            void main()
            {{
                out_color = {color_assign}            
            }};
        """.format(
            color_assign=color_assign,
            color_in=color_in
        )

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

    def color(self, r: float, g: float, b: float, a: float):
        assert self.has_colors
        offset = self.vertex_id + self.color_offset
        self.vertices[offset] = r
        self.vertices[offset + 1] = g
        self.vertices[offset + 2] = b
        self.vertices[offset + 3] = a

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
        self.vao.delete()
        self.vbo.delete()
        self.shader.delete()
