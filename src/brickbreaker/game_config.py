WIDTH: int = 1024  # pixels
HEIGHT: int = 768  # pixels

WORLD_WIDTH: float = 32  # world units
WORLD_HEIGHT: float = 24  # world units
WORLD_CENTER_X: float = WORLD_WIDTH/2  # world units
WORLD_CENTER_Y: float = WORLD_HEIGHT/2  # world units

LEFT_PAD = 0.5  # world units
TOP_PAD = 2.5  # world units

BRICK_WIDTH = 2.125  # world units
BRICK_HEIGHT = 1.0  # world units

ROW_SPACING = 0.5  # world units
ROW_COUNT = 6  # count

COLUMN_SPACING = 0.5  # world units
COLUMN_COUNT = 12  # count

PADDLE_MIN_WIDTH = 1.2
PADDLE_START_WIDTH = 3  # world units
PADDLE_MAX_WIDTH = 4.8
PADDLE_HEIGHT = 1  # world units
PADDLE_START_X = (WORLD_WIDTH - PADDLE_START_WIDTH) / 2  # world units
PADDLE_START_Y = 1  # world units
PADDLE_VELOCITY_X = 15  # world units
PADDLE_RESIZE_FACTOR = 0.15  # percentage
PADDLE_EXPAND_SHRINK_SPEED = 6

BALL_SIZE = 0.8  # world units
BALL_HALF_SIZE = BALL_SIZE / 2
BALL_START_X = PADDLE_START_X + (PADDLE_START_WIDTH - BALL_SIZE) / 2
BALL_START_Y = PADDLE_START_Y + PADDLE_HEIGHT
BALL_MIN_SPEED = 10
BALL_START_SPEED = 16
BALL_MAX_SPEED = 22
BALL_SPEED_FACTOR = 0.15  # 15%
BALL_START_ANGLE = 60  # degrees
