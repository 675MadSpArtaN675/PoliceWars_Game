from ...sprites_types import SimpleSprite
from ..abstract_objects import ClickableObject

from ..units import MeleeUnit

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

    def click(self):
        if self._once_enter and self._on_click is not None:
            unit, is_need_clear = self._on_click()

            if unit is not None and not is_need_clear:
                self.place_unit(unit)

            elif is_need_clear:
                self.delete_unit()

    def place_unit(self, unit: MeleeUnit):
        if self._is_can_place and (self._unit is None or self._unit.is_dead()):
            unit.set_position(self._position.copy())
            self._unit = unit

    def delete_unit(self):
        self._unit.destroy()
        self._unit = None

    def clear(self):
        if not self._unit.is_dead():
            self.delete_unit()

    def get_unit(self):
        return self._unit
