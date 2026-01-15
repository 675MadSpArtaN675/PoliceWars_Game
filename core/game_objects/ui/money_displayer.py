from ..abstract_objects import ClickableObject
from ...sprites_types import Text

from utility_classes import Point, Size

import pygame as pg


class MoneyDisplay(ClickableObject):
    _money_pattern: str
    _font: Text

    def __init__(
        self,
        screen: pg.Surface,
        surface_size: Size,
        font_size: int,
        font_name: str,
        color: pg.Color,
        money_pattern: str,
        position: Point,
        depth: int,
    ):
        self._font = Text(
            surface_size.width,
            surface_size.height,
            money_pattern,
            font_name,
            font_size,
            color,
            is_alpha=True,
        )

        super().__init__(
            screen=screen,
            sprite=self._font,
            secondary_sprite=None,
            position=position,
            depth=depth,
        )

        self._money_pattern = money_pattern

    @property
    def money_print_pattern(self):
        return self._money_pattern

    @money_print_pattern.setter
    def money_print_pattern(self, value: str):
        self._money_pattern = value

    def render(self, **kwargs):
        money_count = kwargs.get("money_count", 0)
        money_print_string = self._money_pattern.format(money_count)

        self._font.text = money_print_string

        super().render(**kwargs)
