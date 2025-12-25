from utility_classes.point import Point
from utility_classes.size import Size

from ..sprites_types import SimpleSprite

from typing import Callable

import pygame as pg


class GameObject:
    _type = "object"
    _display_name = "GameObject"
    _is_dead: bool = False

    _on_render: Callable = None

    _screen_to_render: pg.Surface
    _sprite: SimpleSprite

    _position: Point
    _depth: int = 0

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        self._position = position

        self._screen_to_render = screen
        self._sprite = sprite

        self._depth = depth

    @property
    def type_name(self):
        return self._display_name

    @property
    def display_name(self):
        return self._display_name

    @property
    def center(self):
        return self._sprite.rect.center

    def render(self):
        if not self._is_dead:
            self._sprite.rect.x, self._sprite.rect.y = self._position.to_tuple()

            self._sprite.update()
            self._screen_to_render.blit(self._sprite.image, self._sprite.rect)

            if self._on_render is not None:
                self._on_render()

    def destroy(self):
        self._sprite.kill()
        self._is_dead = True

    def is_dead(self):
        return self._is_dead

    def get_object_type(self):
        return self._type

    def get_display_name(self):
        return self._display_name

    def on_render_bind(self, function: Callable):
        self._on_render = function

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

    def set_sprite(self, value: SimpleSprite):
        self._sprite = value

    def get_sprite(self):
        return self._sprite

    def get_depth(self):
        return self._depth

    def set_depth(self, value: int):
        self._depth = value

    def copy(self):
        object_copy = GameObject(
            self._screen_to_render,
            self._sprite.copy(),
            position=self._position.copy(),
            depth=self._depth,
        )

        self._copy_protected_attrs(object_copy)

        return object_copy

    def _copy_protected_attrs(self, object_copy: object):
        attrs = ["_on_render", "_is_dead"]

        for attribute in attrs:
            self_attr_value = getattr(self, attribute)
            setattr(object_copy, self_attr_value)
