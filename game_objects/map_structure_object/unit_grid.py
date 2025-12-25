from utility_classes.point import Point
from game_objects.sprites_types import SimpleSprite
from game_objects.abstract_objects import GameObject

from .unit_line import UnitLine

import pygame as pg


class UnitGrid(GameObject):
    _selected_sprite: SimpleSprite = None

    _row_count: int = 0
    _column_count: int = 0

    _grid: list[UnitLine] = None

    def __init__(
        self,
        screen: pg.Surface,
        rows: int,
        columns: int,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, None, position=position, depth=depth)

        self._row_count = rows
        self._column_count = columns
        self._grid = []

    def __getitem__(self, first_key: int, second_key: int):
        if self.__validate_key(first_key) and self.__validate_key(second_key):
            line = self._grid[first_key]

            return line[second_key]

        raise IndexError(
            f"Line index out of range. Index must be in range from 1 to {self._row_count} for rows and in range from 1 to {self._column_count} for columns."
        )

    def __validate_key(self, key):
        return key > 1 and key <= self._cell_count

    def render(self):
        for line in self._grid:
            line.render()

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

    @cell_sprite.setter
    def selected_cell_sprite(self, value: SimpleSprite):
        self._selected_sprite = value

    def build(self):
        if (
            self._screen_to_render is not None
            and self.row_count > 0
            and self._column_count > 0
            and self._sprite is not None
            and self._selected_sprite is not None
        ):
            self._grid = []
            pos = self._position.copy()
            height = self._sprite.rect.height

            for _ in range(self._row_count):
                line = UnitLine(
                    self._screen_to_render,
                    self._sprite.copy(),
                    self._selected_sprite.copy(),
                    self._column_count,
                    position=pos + Point(0, height),
                    depth=self._depth - 1,
                )
                line.build()

                self._grid.append(line)
