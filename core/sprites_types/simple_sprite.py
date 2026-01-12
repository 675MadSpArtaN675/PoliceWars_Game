from utility_classes import Point

from .sprite_base import SpriteBase
from .data import ImageOptions, FlipSide

import pygame as pg


class SimpleSprite(SpriteBase):
    _data: ImageOptions = None

    _color: pg.Color = None

    def __init__(
        self,
        width: int,
        height: int,
        color: pg.Color = pg.Color(255, 255, 255),
        data: ImageOptions = None,
        is_alpha: bool = True,
    ):
        super().__init__(
            width,
            height,
            is_alpha,
        )

        if data is not None:
            self._data = data
            self._source_size = data.get_source_size()

        self._color = color

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def update(self, *args, **kwargs):
        if (
            self._data is not None
            and self._data.get_image() is not None
            and self._data.position is not None
        ):
            self._image.blit(
                pg.transform.flip(self._data.get_image(), *self._data.flip.value),
                self._data.position.to_tuple(),
            )

        elif self._color is not None:
            self._image.fill(self._color)

    def set_size(self, width: int, height: int):
        self._image = pg.Surface((width, height))
        self._rect = self._image.get_rect()

    def get_size(self):
        return self._rect.width, self._rect.height

    def flip(self, how: FlipSide):
        if type(how) == FlipSide:
            self._data.flip = how
            self._data.position = self._flip_position(self._data.position)

    def _flip_position(self, position: Point):
        width, height = self._source_size.to_tuple()
        enum_value = self._data.flip.value

        vertical_coof = width * enum_value[0]
        horizontal_coof = height * enum_value[1]

        return Point(vertical_coof, horizontal_coof) - position.copy()

    def copy(self):
        width = self._rect.width
        height = self._rect.height
        data = self._data

        if data is not None:
            data = self._data.copy()

        sprite_copy = SimpleSprite(width, height, data=data)

        sprite_copy._image = self._image.copy()
        sprite_copy._rect = self._image.get_rect()
        sprite_copy._color = pg.Color(self._color.r, self._color.g, self._color.b)

        return sprite_copy
