from ..abstract_objects import GameObject
from ..sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class PoliceDeadZone(GameObject):
    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, sprite, position=position, depth=depth)
