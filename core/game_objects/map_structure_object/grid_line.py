from ..abstract_objects import GameObject

from utility_classes.point import Point

import pygame as pg


class GridLine(GameObject):
    _game_object: GameObject = None

    _object_list: list[GameObject]
    _cell_count: int = 0

    def __init__(
        self,
        screen: pg.Surface,
        cell_count: int,
        game_object: GameObject,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, None, position=position, depth=depth)

        self._cell_count = cell_count
        self._object_list = []
        self._game_object = game_object

    def __getitem__(self, key: int):
        if key >= 0 and key < self._cell_count:
            return self._unit_cells[key - 1]

        raise IndexError(
            f"Line index out of range. Index must be in range from 1 to {self._cell_count}"
        )

    def __len__(self):
        return len(self._object_list)

    @property
    def game_object(self):
        return self._game_object

    @game_object.setter
    def game_object(self, game_object: GameObject):
        self._game_object = game_object

    @property
    def cell_count(self):
        return self._cell_count

    @cell_count.setter
    def cell_count(self, value: int):
        self._cell_count = value

    def clear_object(self):
        self._game_object = None

    def clear_line(self):
        self._object_list.clear()

    def build(self, place_by_column: bool = False):
        line_objects = []

        pos = self._position.copy()
        for _ in range(self._cell_count):
            game_object = self._game_object.copy()
            game_object.set_position(pos.copy())
            game_object.set_depth(self._depth + 1)

            line_objects.append(game_object)

            if place_by_column:
                pos += Point(0, game_object.get_sprite().rect.height)
            else:
                pos += Point(game_object.get_sprite().rect.width, 0)

        self._object_list.extend(line_objects)
