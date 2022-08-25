import pyrr


class OrthographicCamera:
    def __init__(self) -> None:
        self.viewport_width = 0   # world units
        self.viewport_height = 0  # world units
        self.zoom = 1.0
        self.position = pyrr.Vector3([0.0, 0.0, 0.0])
        self.direction = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.near = 0
        self.far = 100
        self.combined = None

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y

    def update(self) -> None:
        projection = pyrr.matrix44.create_orthogonal_projection(
            self.zoom * -self.viewport_width/2,
            self.zoom * (self.viewport_width/2),
            self.zoom * (-self.viewport_height/2),
            self.zoom * (self.viewport_height/2),
            self.near,
            self.far
        )
        view = pyrr.matrix44.create_look_at(
            self.position,
            self.position + self.direction,
            self.up
        )
        self.combined = pyrr.matrix44.multiply(view, projection)
