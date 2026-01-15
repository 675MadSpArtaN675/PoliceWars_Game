from .sprite_base import SpriteBase

from utility_classes import Point

import pygame as pg


class Text(SpriteBase):
    _text: str = None
    _font: pg.font.Font = None

    _color: pg.Color = None
    _background_color: pg.Color = None

    _max_width: int = 0
    _max_height: int = 0

    _min_width: int = 0
    _min_height: int = 0

    def __init__(
        self,
        width: int,
        height: int,
        text: str,
        font: str,
        font_size: int,
        color: pg.Color,
        max_width: int = 0,
        max_height: int = 0,
        min_width: int = 0,
        min_height: int = 0,
        background_color: pg.Color = None,
        is_alpha: bool = False,
    ):
        super().__init__(width, height, is_alpha)

        self._text = text
        self._font = pg.font.Font(font, font_size)

        self._color = color
        self._background_color = background_color

        self._max_width = max_width
        self._max_height = max_height
        self._min_width = min_width
        self._min_height = min_height

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def font(self):
        return self._font

    def update(self, *args, **kwargs):
        if (
            self._text is not None
            and self._font is not None
            and self._color is not None
        ):
            size = self._font.size(self._text)
            self.set_size(*size)

            surface_text = self._font.render(
                self._text,
                True,
                self._color,
                self._background_color,
            )

            self._image.blit(surface_text, (0, 0))

    def set_size(self, width: int, height: int):
        width_ = self.__check_value(width, self._max_width, self._min_width)
        height_ = self.__check_value(height, self._max_height, self._min_height)

        super().set_size(width_, height_)

    def __check_value(self, value: int, max_value: int, min_value: int):
        if value < min_value and min_value != 0:
            return min_value

        elif value > max_value and max_value != 0:
            return max_value

        else:
            return value
