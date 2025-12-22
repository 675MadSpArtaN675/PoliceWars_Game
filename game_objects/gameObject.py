from utility_classes.point import Point
from utility_classes.size import Size

from sprites_types.simple_sprite import SimpleSprite

import pygame as pg


class GameObject:
    _screen_to_render: pg.Surface
    _sprite: SimpleSprite

    _position: Point

    def __init__(
        self, screen: pg.Surface, sprite: SimpleSprite, /, position: Point = Point()
    ):
        self._position = position

        self._screen_to_render = screen
        self._sprite = sprite

    def render(self):
        self._sprite.Rect.x, self._sprite.Rect.y = self._position.to_tuple()

        self._sprite.update()
        self._screen_to_render.blit(self._sprite.Image, self._sprite.Rect)

    def set_color(self, color: pg.Color):
        self._color = color

    def get_color(self):
        return self._color

    def set_position(self, position: Point):
        self._position = position

    def get_position(self):
        return self._position

    def set_size(self, size: Size):
        self._size = size

    def get_size(self):
        return self._size
