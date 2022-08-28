from .vertex_buffer_layout import VertexBufferLayout
from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .shader import Shader
from .color import Color
import numpy as np
from OpenGL.GL import *


class VertexCounter:
    def __init__(self, element_count) -> None:
        self.element_count = element_count
        self.vertex_id = 0
        self.num_vertices = 0

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, exc_tb):
        self.vertex_id += self.element_count
        self.num_vertices += 1

    def offset(self, value):
        return self.vertex_id + value

    def reset(self):
        self.vertex_id = 0
        self.num_vertices = 0


class ImmediateModeRenderer:
    COLOR_ATTRIB = "a_color"
    COLOR_VARY = "v_color"
    VERTEX_ATTRIB = "a_texture"
    VERTEX_VARY = "v_texture"
    POSITION_ATTRIB = "a_position"

    def __init__(self, max_vertices: int, has_colors: bool, has_texture: bool) -> None:
        self.has_colors = has_colors
        self.has_texture = has_texture
        self.max_vertices = max_vertices
        self.proj_model_view = None

        # offsets
        self.vertex_offset = 0
        self.color_offset = 0
        self.texture_offset = 0

        # shader
        self.shader = Shader(
            self.create_vertex_shader(has_colors, has_texture),
            self.create_fragment_shader(has_colors, has_texture)
        )

        # vbo layout
        self.vbo_layout = VertexBufferLayout()
        self.vbo_layout.push_float(3, self.POSITION_ATTRIB)

        # optional attributes
        if has_colors:
            self.color_offset = self.vbo_layout.count
            self.vbo_layout.push_float(4, self.COLOR_ATTRIB)

        if has_texture:
            self.texture_offset = self.vbo_layout.count
            self.vbo_layout.push_float(2, self.VERTEX_ATTRIB)

        self.vertex_counter = VertexCounter(self.vbo_layout.count)

        # vbo
        self.vertices = np.zeros(
            max_vertices * self.vbo_layout.count,
            dtype=np.float32
        )
        self.vbo = VertexBuffer(self.vertices)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(self.vbo, self.vbo_layout, self.shader)

    def contains_vertices(self):
        return self.vertex_counter.num_vertices > 0

    def create_vertex_shader(self, has_colors, has_texture):
        # color
        color_attribute = f"in vec4 {self.COLOR_ATTRIB};" if has_colors else ""
        color_out = f"out vec4 {self.COLOR_VARY};" if has_colors else ""
        color_assign = f"{self.COLOR_VARY} = {self.COLOR_ATTRIB};" if has_colors else ""

        # texture
        texture_attribute = f"in vec2 {self.VERTEX_ATTRIB};" if has_texture else ""
        texture_out = f"out vec2 {self.VERTEX_VARY};" if has_texture else ""
        texture_assign = f"{self.VERTEX_VARY} = {self.VERTEX_ATTRIB};" if has_texture else ""

        return f"""
            #version 330 core
            in vec4 {self.POSITION_ATTRIB};
            {color_attribute}
            {texture_attribute}
            {color_out}
            {texture_out}
            uniform mat4 u_projTrans;
            void main()
            {{
                gl_Position = u_projTrans * {self.POSITION_ATTRIB};
                {color_assign}
                {texture_assign}
            }}
        """

    def create_fragment_shader(self, has_colors, has_texture):
        # color
        color_in = f"in vec4 {self.COLOR_VARY};" if has_colors else ""
        color_assign = f"{self.COLOR_VARY};" if has_colors else "vec4(1.0);"

        # texture
        texture_in = f"in vec2 {self.VERTEX_VARY};" if has_texture else ""
        texture_sampler = "uniform sampler2D s_texture;" if has_texture else ""
        texture_multiply = f"out_color *= texture(s_texture, {self.VERTEX_VARY});" if has_texture else ""

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
        if not self.contains_vertices():
            return

        self.vao.bind()
        self.vbo.set_data(
            self.vertices,
            self.vertex_counter.num_vertices * self.vbo_layout.stride
        )

        self.shader.set_uniform_mat4f("u_projTrans", self.proj_model_view)
        glDrawArrays(self.primitive_type, 0, self.vertex_counter.num_vertices)
        self.vertex_counter.reset()

    def start_new_vertex(self):
        return self.vertex_counter

    def color(self, color: Color):
        assert self.has_colors
        offset = self.vertex_counter.offset(self.color_offset)
        self.vertices[offset] = color.r
        self.vertices[offset + 1] = color.g
        self.vertices[offset + 2] = color.b
        self.vertices[offset + 3] = color.a

    def texture(self, u: float, v: float):
        assert self.has_texture
        offset = self.vertex_counter.offset(self.texture_offset)
        self.vertices[offset] = u
        self.vertices[offset + 1] = v

    def vertex(self, x: float, y: float, z: float):
        idx = self.vertex_counter.offset(self.vertex_offset)
        self.vertices[idx] = x
        self.vertices[idx + 1] = y
        self.vertices[idx + 2] = z

    def free_vertices_count(self):
        return self.max_vertices - self.vertex_counter.num_vertices

    def dispose(self):
        self.vao.delete()
        self.vbo.delete()
        self.shader.delete()
