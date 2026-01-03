from typing import Callable

from .creator import Creator
from ..game_loop_controller import GameLoopController

from game_objects.abstract_objects import GameObject, ProcessableObject

from game_objects.sprites_types import SimpleSprite
from game_objects.map_structure_object import UnitGrid
from game_objects.units import MeleeUnit

from ..objects_data import UnitList, UnitToSpawn, UnitFraction
from game_objects.map_structure_object import EnemySpawner

from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


class MapObjectsCreator(Creator):
    _objects: list[ProcessableObject] = None
    _clickable_objects: list[GameObject] = None

    _grid_size: Size = Size()
    _placer: Callable[[None], GameObject] = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        grid_size: Size,
        start_objects: list[GameObject] = (),
        start_clickable_objects: list[GameObject] = (),
    ):
        self._game_cycle = game_cycle
        self._grid_size = grid_size
        self._objects = list(start_objects)
        self._clickable_objects = list(start_clickable_objects)

    @property
    def func_placer(self):
        return self._placer

    @func_placer.setter
    def func_placer(self, func: Callable[[None], GameObject]):
        self._placer = func

    def create(self):
        unit_grid = self._create_unit_grid(
            SimpleSprite(50, 50, pg.Color(255, 0, 0)),
            SimpleSprite(50, 50, pg.Color(0, 0, 255)),
            Point(100, 225),
        )

        self._clickable_objects.append(unit_grid)

        units = UnitList(
            [
                UnitToSpawn(
                    MeleeUnit(
                        self._game_cycle.screen,
                        SimpleSprite(50, 50, pg.Color(255, 255, 255)),
                        100,
                        10,
                        -10,
                        UnitFraction.Terrorists,
                    ),
                    50,
                ),
                UnitToSpawn(
                    MeleeUnit(
                        self._game_cycle.screen,
                        SimpleSprite(50, 50, pg.Color(255, 255, 125)),
                        100,
                        15,
                        -5,
                        UnitFraction.Terrorists,
                    ),
                    10,
                ),
                UnitToSpawn(
                    MeleeUnit(
                        self._game_cycle.screen,
                        SimpleSprite(50, 50, pg.Color(255, 255, 125)),
                        125,
                        25,
                        -2,
                        UnitFraction.Terrorists,
                    ),
                    10,
                ),
            ]
        )

        for point in unit_grid.get_positions_of_last_points():
            point.x += 50
            spawner = EnemySpawner(
                self._game_cycle.screen, SimpleSprite(50, 50), units, position=point
            )
            self._objects.append(spawner)

        return self._objects, self._clickable_objects

    def process_object(self, object_: ProcessableObject, delta_time: int, **kwargs):
        if object_ is not None and issubclass(type(object_), ProcessableObject):
            object_.process(delta_time, **kwargs)

    def _create_unit_grid(
        self,
        cell_sprite: SimpleSprite,
        selected_cell_s_sprite: SimpleSprite,
        position: Point,
    ):
        unit_grid = UnitGrid(
            self._game_cycle.screen,
            self._grid_size.width,
            self._grid_size.height,
            position,
            -100,
        )

        unit_grid.cell_sprite = cell_sprite
        unit_grid.selected_cell_sprite = selected_cell_s_sprite

        if self._placer is not None:
            unit_grid.on_click_bind(self._placer)

        unit_grid.build()

        return unit_grid

    def get_objects(self):
        return self._objects, self._clickable_objects
