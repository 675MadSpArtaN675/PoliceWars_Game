from .abstract_objects import ClickableObject
from .abstract_objects.sprites_types import SimpleSprite
from .units.gunner import Unit

from utility_classes.point import Point

import pygame as pg


class Cell(ClickableObject):
    _type = "cell"
    _display_name = "Cell"

    _unit: Unit = None

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        secondary_sprite: SimpleSprite,
        /,
        position: Point = Point(),
    ):
        super().__init__(screen, sprite, secondary_sprite, position)

    def render(self):
        super().render()

        if self._unit is not None:
            self._unit.render()

    def place_unit(self, unit: Unit):
        if unit is not None and self._unit is None:
            print(self._unit, unit)
            self._unit = unit

    def delete_unit(self):
        self._unit = None

    def get_unit(self):
        return self._unit
