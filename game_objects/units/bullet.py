from ..sprites_types import SimpleSprite
from .melee import MeleeUnit
from utility_classes.point import Point

import pygame as pg


class Bullet(MeleeUnit):
    _type = "projectile"
    _display_name = "Bullet"

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        /,
        position: Point = Point(),
        restricted_objects=[],
        depth: int = 0,
    ):
        super().__init__(
            screen,
            sprite,
            health,
            damage,
            speed,
            position=position.copy(),
            restricted_objects=restricted_objects,
            depth=depth,
        )
