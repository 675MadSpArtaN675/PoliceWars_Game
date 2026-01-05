from ..sprites_types import SimpleSprite

from utility_classes.point import Point

from dataclasses import dataclass


@dataclass
class ObjectData:
    sprite: SimpleSprite
    position: Point
    depth: int = 0


@dataclass
class ClickableObjectData:
    primary_sprite: SimpleSprite
    secondary_sprite: SimpleSprite
    position: Point
    depth: int = 0
