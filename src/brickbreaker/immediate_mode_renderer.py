from .vertex_buffer_layout import VertexBufferLayout
from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .shader import Shader
import numpy as np
from OpenGL.GL import *


class ImmediateModeRenderer:
    def __init__(self, max_vertices: int, has_colors: bool, has_texture: bool) -> None:
        self.has_colors = has_colors
        self.has_texture = has_texture
        self.max_vertices = max_vertices
        self.vertex_id = 0
        self.num_vertices = 0
        self.proj_model_view = None
        self.color_offset = 0
        self.texture_offset = 0

        # shader
        self.shader = Shader(
            self.create_vertex_shader(has_colors, has_texture),
            self.create_fragment_shader(has_colors, has_texture)
        )

        # vbo layout
        self.vbo_layout = VertexBufferLayout()
        self.vbo_layout.push_float(3, "a_position")

        # optional attributes
        if has_colors:
            self.color_offset = self.vbo_layout.count
            self.vbo_layout.push_float(4, "a_color")

        if has_texture:
            self.texture_offset = self.vbo_layout.count
            self.vbo_layout.push_float(2, "a_texture")

        # vbo
        self.vertices = np.zeros(
            max_vertices * self.vbo_layout.count,
            dtype=np.float32
        )
        self.vbo = VertexBuffer(self.vertices)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(self.vbo, self.vbo_layout, self.shader)

    def create_vertex_shader(self, has_colors, has_texture):
        # color
        color_attribute = "in vec4 a_color;" if has_colors else ""
        color_out = "out vec4 v_color;" if has_colors else ""
        color_assign = "v_color = a_color;" if has_colors else ""

        # texture
        texture_attribute = "in vec2 a_texture;" if has_texture else ""
        texture_out = "out vec2 v_texture;" if has_texture else ""
        texture_assign = "v_texture = a_texture;" if has_texture else ""

        return f"""
            #version 330 core
            in vec4 a_position;
            {color_attribute}
            {texture_attribute}
            {color_out}
            {texture_out}
            uniform mat4 u_projTrans;
            void main()
            {{
                gl_Position = u_projTrans * a_position;
                {color_assign}
                {texture_assign}
            }}
        """

    def create_fragment_shader(self, has_colors, has_texture):
        # color
        color_in = "in vec4 v_color;" if has_colors else ""
        color_assign = "v_color;" if has_colors else "vec4(1.0, 1.0, 1.0, 1.0)"

        # texture
        texture_in = "in vec2 v_texture;" if has_texture else ""
        texture_sampler = "uniform sampler2D s_texture;" if has_texture else ""
        texture_multiply = "out_color *= texture(s_texture, v_texture);" if has_texture else ""

        return f"""
            #version 330 core
            out vec4 out_color;
            {color_in}
            {texture_in}
            {texture_sampler}
            void main()
            {{
                out_color = {color_assign}
                {texture_multiply}
            }};
        """

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

    def texture(self, u: float, v: float):
        assert self.has_texture
        offset = self.vertex_id + self.texture_offset
        self.vertices[offset] = u
        self.vertices[offset + 1] = v

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
