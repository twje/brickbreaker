from brickbreaker.core.shape_renderer import ShapeRenderer
from brickbreaker.core.rectangle import Rectangle
from brickbreaker.core.polygon import Polygon


def rect(renderer: ShapeRenderer, rect: Rectangle):
    renderer.rect(
        rect.x,
        rect.y,
        rect.width,
        rect.height
    )


def polygon(renderer: ShapeRenderer, polygon: Polygon):
    renderer.polygon(polygon.get_transformed_vertices())
