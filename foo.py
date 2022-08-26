has_colors = False

color_attribute = "in vec4 a_color;" if has_colors else ""
color_out = "out vec4 v_color;" if has_colors else ""
color_assign = "v_color = a_color;" if has_colors else ""

foo = """
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
print(foo)
