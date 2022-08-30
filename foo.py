# from dataclasses import dataclass


# def create_vertex_shader(has_colors, has_texture):
#     # color
#     color_attribute = "in vec4 a_color;" if has_colors else ""
#     color_out = "out vec4 v_color;" if has_colors else ""
#     color_assign = "v_color = a_color;" if has_colors else ""

#     # texture
#     texture_attribute = "in vec2 a_texture;" if has_texture else ""
#     texture_out = "out vec4 v_texture;" if has_texture else ""
#     texture_assign = "v_texture = a_texture;" if has_texture else ""

#     return f"""
#         #version 330 core
#         in vec4 a_position;
#         {color_attribute}
#         {texture_attribute}
#         {color_out}
#         {texture_out}
#         uniform mat4 u_projTrans;
#         void main()
#         {{
#             gl_Position = u_projTrans * a_position;
#             {color_assign}
#             {texture_assign}
#         }}
#     """


# def create_fragment_shader(has_colors, has_texture):
#     # color
#     color_in = "in vec4 v_color;" if has_colors else ""
#     color_assign = "v_color;" if has_colors else "vec4(1.0, 1.0, 1.0, 1.0)"

#     # texture
#     texture_in = "in vec4 v_texture;" if has_texture else ""
#     texture_sampler = "uniform sampler2D s_texture;" if has_texture else ""
#     texture_multiply = "out_color *= texture(s_texture, v_texture);" if has_texture else ""

#     return f"""
#         #version 330 core
#         out vec4 out_color;
#         {color_in}
#         {texture_in}
#         {texture_sampler}
#         void main()
#         {{
#             out_color = {color_assign}
#             {texture_multiply}
#         }};
#     """


# # vertex = create_vertex_shader(False, False)
# # fragment = create_fragment_shader(False, False)

# # print(vertex)
# # print("")
# # print(fragment)


# @dataclass
# class Color:
#     r: float = 1
#     g: float = 1
#     b: float = 1
#     a: float = 1

#     def __iter__(self) -> None:
#         return iter([self.r, self.g, self.b, self.a])

#     def copy(self):
#         return Color(self.r, self.g, self.b, self.a)


# color = Color()
# for x in color:
#     print(x)


class Foo:
    def __init__(self) -> None:
        pass

    def __eq__(self, __o: object) -> bool:
        print("FF")
        return False

print(Foo() is Foo())