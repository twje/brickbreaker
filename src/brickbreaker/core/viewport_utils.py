from .fit_viewport import FitViewport
from .shape_renderer import ShapeRenderer
from . import color


def debug_pixels_per_unit(viewport: FitViewport):
    pass


def draw_grid(viewport: FitViewport, renderer: ShapeRenderer, draw_world_units=False):
    old_color = renderer.color.copy()

    cell_size = 1
    world_width = viewport.world_width
    world_height = viewport.world_height
    double_world_width = viewport.world_width * 2
    double_world_height = viewport.world_height * 2

    renderer.set_projection_matrix(viewport.camera.combined)
    renderer.begin(ShapeRenderer.ShapeType.Line)

    renderer.color = color.WHITE

    if draw_world_units:
        # draw vertical lines
        for x in range(-double_world_width, double_world_height, cell_size):
            renderer.line(x, -double_world_height, x, double_world_height)

        # draw horizontal lines
        for y in range(-double_world_height, double_world_height, cell_size):
            renderer.line(-double_world_width, y, double_world_width, y)

    # draw 0/0 lines
    renderer.color = color.RED
    renderer.line(0, -double_world_height, 0, double_world_height)

    renderer.color = color.BLUE
    renderer.line(0, -double_world_height, 0, double_world_height)
    renderer.line(-double_world_width, 0, double_world_width, 0)

    # draw world bounds
    renderer.color = color.GREEN
    renderer.line(0, world_height, world_width, world_height)
    renderer.line(world_width, 0, world_width, world_height)

    renderer.end()
    renderer.color = old_color
