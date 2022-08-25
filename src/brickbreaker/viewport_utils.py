from .shape_renderer import ShapeRenderer


def draw_grid(viewport, renderer):
    cell_size = 1
    world_width = viewport.world_width
    world_height = viewport.world_height
    double_world_width = viewport.world_width * 2
    double_world_height = viewport.world_height * 2

    renderer.set_projection_matrix(viewport.camera.combined)
    renderer.begin(ShapeRenderer.ShapeType.Line)

    # draw vertical lines
    for x in range(-double_world_width, double_world_height, cell_size):
        renderer.line(x, -double_world_height, x, double_world_height)

    # draw horizontal lines
    for y in range(-double_world_height, double_world_height, cell_size):
        renderer.line(-double_world_width, y, double_world_width, y)

    renderer.end()
