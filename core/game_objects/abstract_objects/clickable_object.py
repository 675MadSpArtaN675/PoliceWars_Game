from ...sprites_types import SimpleSprite

from .game_object import GameObject

from utility_classes.point import Point

from typing import Callable
import pygame as pg


class ClickableObject(GameObject):
    _type = "clickable_object"
    _display_name = "GameObject"

    _secondary_sprite: SimpleSprite = None

    _cursor_on_object: bool = False
    _once_enter: bool = False
    _one_render: bool = False
    _rendering: bool = False

    _clicked: bool = False

    _on_click: Callable = None
    _on_enter: Callable = None
    _on_exit: Callable = None

    def __init__(
        self,
        *,
        screen: pg.Surface = None,
        sprite: SimpleSprite = None,
        secondary_sprite: SimpleSprite = None,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen=screen, sprite=sprite, position=position, depth=depth)
        self._secondary_sprite = secondary_sprite

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

    def render(self, **kwargs):
        if self._is_renderable and not self.is_dead():
            self._sprite.update(**kwargs)
            self._set_sprite_rect_pos(self._sprite, self._position)

            sprite_image = self._sprite.image.copy()
            sprite_rect = self._sprite.rect

            if self._rendering and self._secondary_sprite is not None:
                self._secondary_sprite.update(**kwargs)
                sprite_image.blit(self._secondary_sprite.image, (0, 0))

            self._screen_to_render.blit(sprite_image, sprite_rect)

            if self._once_enter and not self._one_render:
                self._rendering = True
                self._one_render = True

            elif not self._once_enter and self._one_render:
                self._rendering = False
                self._one_render = False

            if self._on_render is not None:
                self._on_render()

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

    def __deepcopy__(self, memo: dict[int, object]):
        object_copy = super().__deepcopy__(memo)

        object_copy._secondary_sprite = self._copy_linked_objects(
            self._secondary_sprite
        )

        object_copy._on_click = self._on_click
        object_copy._on_enter = self._on_enter
        object_copy._on_exit = self._on_exit

        return object_copy
