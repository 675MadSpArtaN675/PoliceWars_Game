from ..abstract_objects import GameObject

from .grid_line import GridLine

from utility_classes.point import Point

import pygame as pg


class Grid(GameObject):
    _game_object: GameObject = None

    _row_count: int = 0
    _column_count: int = 0

    _grid: list[GridLine] = None

    def __init__(
        self,
        screen: pg.Surface,
        game_object: GameObject,
        rows: int,
        columns: int,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, None, position=position, depth=depth)

        self._row_count = rows
        self._column_count = columns
        self._grid = []
        self._game_object = game_object

    def build(self, place_by_column: bool = False):
        lines = []
        pos = self._position.copy()

        for _ in range(self._row_count):
            line = GridLine(
                self._screen_to_render,
                self._column_count,
                self._game_object,
                pos.copy(),
                self._depth + 1,
            )

            line.build(place_by_column)

            if place_by_column:
                pos += Point(self._game_object.get_sprite().rect.width, 0)
            else:
                pos += Point(0, self._game_object.get_sprite().rect.height)

            lines.append(line)

        self._grid.extend(lines)

    def __getitem__(self, key: int | tuple[int, int]):
        if type(key) == int:
            if self._validate_key(key, self._row_count):
                return self._grid[key - 1]

        elif type(key) == tuple and len(key) > 1:
            first_key = key[0]
            second_key = key[1]

            if self._validate_key(first_key, self._row_count):
                line = self._grid[first_key - 1]

                return line[second_key]

        raise IndexError(
            f"Line index out of range. Index must be in range from 1 to {self._row_count} for rows and in range from 1 to {self._column_count} for columns."
        )

    def _validate_key(self, key: int, len: int):
        return key >= 0 and key < len
