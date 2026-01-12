from utility_classes.point import Point
from utility_classes.size import Size

from ...sprites_types import SimpleSprite, SpriteBase

from typing import Callable

import copy as c

import pygame as pg


class GameObject:
    _type = "object"
    _display_name = "GameObject"

    _is_dead: bool = False
    _is_renderable: bool = True

    _on_render: Callable = None

    _screen_to_render: pg.Surface = None
    _sprite: SimpleSprite = None

    _position: Point = None
    _depth: int = 0

    def __init__(
        self,
        *,
        screen: pg.Surface = None,
        sprite: SimpleSprite = None,
        position: Point = Point(),
        depth: int = 0,
    ):
        self._screen_to_render = screen
        self._sprite = sprite
        self._position = position

        self._depth = depth

    @property
    def is_renderable(self):
        return self._is_renderable

    @is_renderable.setter
    def is_renderable(self, flag: bool):
        self._is_renderable = flag

    @property
    def type_name(self):
        return self._type

    @property
    def display_name(self):
        return self._display_name

    @property
    def center(self):
        return self._sprite.rect.center

    def render(self):
        self._set_sprite_rect_pos(self._sprite, self._position)

        if self.is_renderable and not self._is_dead:
            self._sprite.update()
            self._screen_to_render.blit(self._sprite.image, self._sprite.rect)

            if self._on_render is not None:
                self._on_render()

    def _set_sprite_rect_pos(self, sprite: SpriteBase, position: Point):
        sprite.rect.x, sprite.rect.y = position.to_tuple()

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

        if self._sprite is not None:
            self._sprite.rect.x = position.x
            self._sprite.rect.y = position.y

    def get_position(self):
        return self._position

    def set_size(self, size: Size):
        self._size = size
        self._sprite.rect.width = self._size.width
        self._sprite.rect.height = self._size.height

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
        return c.deepcopy(self)

    def __repr__(self):
        return f"[{self._type}]: {self._sprite} (id: {id(self._sprite)}), {self._position}, {self._depth}."

    def __deepcopy__(self, memo: dict[int, object]):
        object_copy = type(self)(
            screen=self._screen_to_render,
            position=self._copy_linked_objects(self._position),
            depth=self._depth,
        )
        object_copy._sprite = self._copy_linked_objects(self._sprite)

        self._fill_memo(memo, object_copy)

        return object_copy

    def _fill_memo(self, memo: dict[int, object], object_copy: object):
        memo[id(self)] = self
        memo[id(object_copy)] = object_copy

    def _copy_linked_objects(self, object: object):
        if object is not None:
            try:
                return object.copy()
            except AttributeError:
                return c.deepcopy(object)
