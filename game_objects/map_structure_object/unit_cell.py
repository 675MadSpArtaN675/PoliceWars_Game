from ..abstract_objects import ClickableObject
from ..sprites_types import SimpleSprite
from ..units.gunner import MeleeUnit

from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


class Cell(ClickableObject):
    _type = "cell"
    _display_name = "Cell"

    _unit: MeleeUnit = None
    _is_can_place: bool = True

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        secondary_sprite: SimpleSprite,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, sprite, secondary_sprite, position, depth)

    def get_cell_size(self):
        w = self._sprite.rect.width
        h = self._sprite.rect.height

        return Size(w, h)

    def render(self):
        super().render()

        if self._unit is not None:
            self._unit.render()

    def place_unit(self, unit: MeleeUnit):
        if self._is_can_place and unit is not None and self._unit is None:
            self._unit = unit

    def delete_unit(self):
        self._unit = None

    def get_unit(self):
        return self._unit
