from utility_classes.point import Point

from dataclasses import dataclass

from enum import IntEnum, auto

import pygame as pg


class UnitType(IntEnum):
    Melee: int = auto()
    Gunner: int = auto()


class UnitFraction(IntEnum):
    Police: int = auto()
    Terrorists: int = auto()


@dataclass
class UnitData:
    unit_type: UnitType
    fraction: UnitFraction
    textures: dict[str, pg.Surface]
    health: int
    damage: int
    speed: int
    bullet_speed: int
    bullet_spawn_position: Point
    position: Point
    depth: int
