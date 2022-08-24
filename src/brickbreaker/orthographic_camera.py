import pyrr


class OrthographicCamera:
    def __init__(self) -> None:
        self.viewport_width = 0   # world units
        self.viewport_height = 0  # world units
        self.combined = None

    def update(self) -> None:               
        self.combined = pyrr.matrix44.create_orthogonal_projection(
            -self.viewport_width/2,
            self.viewport_width/2,
            -self.viewport_height/2,
            self.viewport_height/2,
            -1000,
            1000
        )