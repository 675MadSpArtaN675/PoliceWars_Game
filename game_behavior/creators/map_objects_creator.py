from typing import Callable

from .creator import Creator
from game_behavior import GameLoopController

from game_objects.sprites_types import SimpleSprite
from game_objects.map_structure_object import UnitGrid
from game_objects.units import MeleeUnit

from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


class MapObjectsCreator(Creator):
    _objects: list[MeleeUnit] = None

    _grid_size: Size = Size()
    _placer: Callable[[None], MeleeUnit] = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        grid_size: Size,
        start_units: list[MeleeUnit] = (),
    ):
        self._game_cycle = game_cycle
        self._grid_size = grid_size
        self._objects = list(start_units)

    @property
    def func_placer(self):
        return self._placer

    @func_placer.setter
    def func_placer(self, func: Callable[[None], MeleeUnit]):
        self._placer = func

    def create(self):
        unit_grid = UnitGrid(
            self._game_cycle.screen,
            self._grid_size.width,
            self._grid_size.height,
            Point(100, 225),
            -100,
        )

        unit_grid.cell_sprite = SimpleSprite(50, 50, pg.Color(255, 0, 0))
        unit_grid.selected_cell_sprite = SimpleSprite(50, 50, pg.Color(0, 0, 255))

        if self._placer is not None:
            unit_grid.on_click_bind(self._placer)

        unit_grid.build()

        self._objects.append(unit_grid)

        return self._objects

    def get_objects(self):
        return self._objects
