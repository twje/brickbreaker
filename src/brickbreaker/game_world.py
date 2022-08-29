from .entity_factory import EntityFactory
from .brick import Brick


class GameWorld:
    def __init__(self, factory: EntityFactory) -> None:
        self.factory = factory
        self.background = factory.create_background()
        self.paddle = factory.create_paddle()
        self.ball = factory.create_ball()
        self.bricks: list[Brick] = []
        self.start_level()

    def start_level(self):
        self.restart()
        self.bricks = self.factory.create_bricks()        

    def restart(self):
        pass
