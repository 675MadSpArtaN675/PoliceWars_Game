from .unit_cell import Cell
from game_objects.abstract_objects import GameObject
from game_objects.sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class UnitLine(GameObject):
    _selection_sprite: SimpleSprite

    _cell_count: int = 0
    _unit_cells: tuple[Cell] | list[Cell] = ()

    def __init__(
        self,
        screen: pg.Surface,
        primary_cell_sprite: SimpleSprite,
        selection_sprite: SimpleSprite,
        cell_count: int,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, primary_cell_sprite, position, depth)
        self._cell_count = cell_count

        if issubclass(type(primary_cell_sprite), SimpleSprite) and issubclass(
            type(selection_sprite), SimpleSprite
        ):
            self._primary_cell_sprite = primary_cell_sprite
            self._selection_sprite = selection_sprite

        else:
            raise TypeError("Incorrect Type for any sprites")

    def render(self):
        for cell in self._unit_cells:
            cell.detect()
            cell.render()

    def build(self):
        if self._cell_count > 0:
            print(self._cell_count)
            self._unit_cells = []

            cell_size = (
                self._primary_cell_sprite.rect.width,
                self._primary_cell_sprite.rect.height,
            )

            position = self._position.copy()
            for _ in range(self._cell_count):
                cell = Cell(
                    self._screen_to_render,
                    self._sprite.copy(),
                    self._selection_sprite.copy(),
                    position=position.copy(),
                    depth=self._depth - 1,
                )

                self._unit_cells.append(cell)
                position += Point(cell_size[0], 0)

    def __getitem__(self, key: int):
        if key > 1 and key <= self._cell_count:
            return self._unit_cells[key - 1]

        raise IndexError(
            f"Line index out of range. Index must be in range from 1 to {self._cell_count}"
        )

    def __len__(self):
        return len(self._unit_cells)
