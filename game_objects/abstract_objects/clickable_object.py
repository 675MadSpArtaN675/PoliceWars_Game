from utility_classes.point import Point
from ..sprites_types import SimpleSprite
from .game_object import GameObject

from typing import Callable
import pygame as pg


class ClickableObject(GameObject):
    _type = "clickable_object"
    _display_name = "GameObject"

    _secondary_sprite: SimpleSprite = None

    _cursor_on_object: bool = False
    _once_enter: bool = False
    _one_render: bool = False
    _clicked: bool = False

    _on_click: Callable = None
    _on_enter: Callable = None
    _on_exit: Callable = None

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        secondary_sprite: SimpleSprite,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, sprite, position=position, depth=depth)

        if secondary_sprite is not None:
            self._secondary_sprite = secondary_sprite
        else:
            self._secondary_sprite = self._sprite

    def on_click_bind(self, function: Callable):
        self._on_click = function

    def on_enter_bind(self, function: Callable):
        self._on_enter = function

    def on_exit_bind(self, function: Callable):
        self._on_exit = function

    def on_curson_button_pos(self, function: Callable):
        self._on_exit = function

    def click(self):
        self._clicked = False

        if self._once_enter and self._on_click is not None:
            self._on_click()
            self._clicked = True

    def is_clicked(self):
        return self._clicked

    def render(self):
        if self._once_enter and not self._one_render:
            self._sprite, self._secondary_sprite = self._secondary_sprite, self._sprite
            self._one_render = True

        elif not self._once_enter and self._one_render:
            self._sprite, self._secondary_sprite = self._secondary_sprite, self._sprite
            self._one_render = False

        super().render()

    def detect(self):
        x, y = pg.mouse.get_pos()
        self.__is_cursor_on_plane(x, y)

    def __is_cursor_on_plane(self, x: int | float, y: int | float):
        coordinate = self.get_position()

        width = self._sprite.rect.width
        height = self._sprite.rect.height

        is_cursor_x_in_zone = x > coordinate.x and x < coordinate.x + width
        is_cursor_y_in_zone = y > coordinate.y and y < coordinate.y + height

        if is_cursor_x_in_zone and is_cursor_y_in_zone:
            if not self._once_enter:
                if self._on_enter is not None:
                    self._on_enter()

                self._once_enter = True
        elif self._once_enter:
            if self._on_exit is not None:
                self._on_exit()

            self._once_enter = False

        self._cursor_on_object = is_cursor_x_in_zone and is_cursor_y_in_zone

    def copy(self):
        object_copy = ClickableObject(
            self._screen_to_render,
            self._sprite.copy(),
            self._secondary_sprite.copy(),
            position=self._position.copy(),
            depth=self._depth,
        )

        self._copy_protected_attrs(object_copy)

        return object_copy

    def _copy_protected_attrs(self, object_copy: object):
        super()._copy_protected_attrs(object_copy)

        attrs = [
            "_cursor_on_object",
            "_once_enter",
            "_one_render",
            "_clicked",
            "_on_click",
            "_on_enter",
            "_on_exit",
        ]

        for attribute in attrs:
            self_attr_value = getattr(self, attribute)
            setattr(object_copy, attribute, self_attr_value)
