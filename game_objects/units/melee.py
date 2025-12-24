from ..abstract_objects import Unit
from ..abstract_objects.sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class MeleeUnit(Unit):
    _type = "melee_unit"
    _display_name = "Melee Unit"

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(
            screen,
            sprite,
            health,
            damage,
            speed,
            position=position,
            depth=depth,
            restricted_objects=[],
        )
