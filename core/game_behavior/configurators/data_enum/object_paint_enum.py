from enum import IntEnum, auto


class ObjectPaintLevel(IntEnum):
    ui = 0
    bullet = auto()
    enemy = auto()
    objects = auto()
