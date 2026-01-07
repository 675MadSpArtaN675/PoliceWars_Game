from .unit_cell import Cell

from ...sprites_types import SimpleSprite
from ..abstract_objects import GameObject

from utility_classes.point import Point

from typing import Callable

import pygame as pg


class UnitLine(GameObject):
    _func_click_performer: Callable = None
    _primary_cell_sprite: SimpleSprite = None
    _selection_sprite: SimpleSprite = None

    _cell_count: int = 0
    _unit_cells: tuple[Cell] | list[Cell] = ()

    def __init__(
        self,
        *,
        screen: pg.Surface,
        primary_cell_sprite: SimpleSprite,
        selection_sprite: SimpleSprite,
        cell_count: int,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(
            screen=screen, sprite=primary_cell_sprite, position=position, depth=depth
        )
        self._cell_count = cell_count

        if issubclass(type(primary_cell_sprite), SimpleSprite) and issubclass(
            type(selection_sprite), SimpleSprite
        ):
            self._primary_cell_sprite = primary_cell_sprite
            self._selection_sprite = selection_sprite

        else:
            raise TypeError("Incorrect Type for any sprites")

    def on_click_bind(self, function: Callable):
        self._func_click_performer = function

    def click(self):
        for cell in self._unit_cells:
            cell.click()

    def detect(self):
        for cell in self._unit_cells:
            cell.detect()

    def render(self):
        for cell in self._unit_cells:
            cell.render()

    def clear(self):
        for cell in self._unit_cells:
            cell.clear()

    def build(self):
        if self._cell_count > 0:
            self._unit_cells = []

            cell_size = (
                self._primary_cell_sprite.rect.width,
                self._primary_cell_sprite.rect.height,
            )

            position = self._position.copy()
            for _ in range(self._cell_count):
                cell = Cell(
                    screen=self._screen_to_render,
                    sprite=self._sprite.copy(),
                    secondary_sprite=self._selection_sprite.copy(),
                    position=position.copy(),
                    depth=self._depth - 1,
                )
                cell.on_click_bind(self._func_click_performer)

                self._unit_cells.append(cell)
                position += Point(cell_size[0], 0)

    def __getitem__(self, key: int):
        if key > 0 and key <= self._cell_count:
            return self._unit_cells[key - 1]

        raise IndexError(
            f"Line index out of range. Index must be in range from 1 to {self._cell_count}"
        )

    def __deepcopy__(self, memo: dict[int, GameObject]):
        object_copy = super().__deepcopy__(memo)

        object_copy._func_click_performer = self._func_click_performer

        object_copy._primary_cell_sprite = self._copy_linked_objects(
            self._primary_cell_sprite
        )
        object_copy._selection_sprite = self._copy_linked_objects(
            self._selection_sprite
        )

        object_copy._cell_count = self._cell_count

        object_copy._unit_cells = self._copy_linked_objects(self._unit_cells)

        return object_copy

    def __len__(self):
        return len(self._unit_cells)
