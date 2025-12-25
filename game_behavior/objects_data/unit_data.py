from utility_classes.point import Point
from .unit_textures_data import TextureData

from dataclasses import dataclass

from enum import IntEnum, auto


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
    textures: dict[str, TextureData]
    health: int
    damage: int
    speed: int
    bullet_speed: int
    bullet_spawn_position: Point
    position: Point
    depth: int
