from dataclasses import dataclass

from utility_classes.point import Point
from game_objects.sprites_types import SimpleSprite


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
