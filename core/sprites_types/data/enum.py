from enum import Enum, IntEnum, auto


class FlipSide(Enum):
    NoFlip = (False, False)
    Horizontal = (True, False)
    Vertical = (False, True)
    Both = (True, True)


class SpriteType(IntEnum):
    Simple = 0
    Animated = auto()
