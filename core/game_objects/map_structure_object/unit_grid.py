from ...sprites_types import SimpleSprite
from ..abstract_objects import GameObject

from .unit_line import UnitLine

from utility_classes.point import Point

from typing import Callable

import pygame as pg


class UnitGrid(GameObject):
    _func_click_performer: Callable = None
    _selected_sprite: SimpleSprite = None

    _row_count: int = 0
    _column_count: int = 0

    _grid: list[UnitLine] = None

    def __init__(
        self,
        *,
        screen: pg.Surface,
        rows: int,
        columns: int,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen=screen, sprite=None, position=position, depth=depth)

        self._row_count = rows
        self._column_count = columns
        self._grid = []

    def __getitem__(self, key: int | tuple[int, int]):

        if type(key) == tuple:
            first_key = key[0]
            second_key = key[1]

            if self.__validate_key(first_key):
                line = self._grid[first_key]

                return line[second_key]

        else:
            if self.__validate_key(key):
                return self._grid[key]

        raise IndexError(
            f"Line index out of range. Index must be in range from 1 to {self._row_count} for rows and in range from 1 to {self._column_count} for columns."
        )

    def __validate_key(self, key):
        return key > 0 and key <= self._row_count

    def on_click_bind(self, function: Callable):
        self._func_click_performer = function

    def click(self):
        for line in self._grid:
            line.click()

    def detect(self):
        for line in self._grid:
            line.detect()

    def render(self):
        for line in self._grid:
            line.render()

    def clear(self):
        for line in self._grid:
            line.clear()

    def get_positions_of_last_points(self):
        return [
            self._grid[line_num][self._column_count].get_position().copy()
            for line_num in range(self._row_count)
        ]

    def get_centers_of_last_points(self):
        return [
            self._grid[line_num][self._column_count].center()
            for line_num in range(self._row_count)
        ]

    @property
    def row_count(self):
        return self._row_count

    @row_count.setter
    def row_count(self, value: int):
        self._row_count = value

    @property
    def column_count(self):
        return self._column_count

    @column_count.setter
    def column_count(self, value: int):
        self._column_count = value

    @property
    def cell_sprite(self):
        return self._sprite

    @cell_sprite.setter
    def cell_sprite(self, value: SimpleSprite):
        self._sprite = value

    @property
    def selected_cell_sprite(self):
        return self._selected_sprite

    @selected_cell_sprite.setter
    def selected_cell_sprite(self, value: SimpleSprite):
        self._selected_sprite = value

    def build(self):
        if (
            self._screen_to_render is not None
            and self._row_count > 0
            and self._column_count > 0
            and self._sprite is not None
            and self._selected_sprite is not None
            and self._func_click_performer is not None
        ):
            self._grid = []
            pos = self._position.copy()
            height = self._sprite.rect.height

            for index in range(self._row_count):
                line = UnitLine(
                    screen=self._screen_to_render,
                    primary_cell_sprite=self._sprite.copy(),
                    selection_sprite=self._selected_sprite.copy(),
                    cell_count=self._column_count,
                    position=pos + Point(0, height),
                    depth=self._depth - index,
                )
                line.on_click_bind(self._func_click_performer)
                line.build()

                self._grid.append(line)

    def __len__(self):
        return len(self._grid)

    def __deepcopy__(self, memo: dict[int, GameObject]):
        object_copy = super().__deepcopy__(memo)

        object_copy._func_click_performer = self._func_click_performer
        object_copy._selected_sprite = self._copy_linked_objects(self._selected_sprite)

        object_copy._row_count = self._row_count
        object_copy._column_count = self._column_count

        object_copy._grid = self._copy_linked_objects(self._grid)

        return object_copy
