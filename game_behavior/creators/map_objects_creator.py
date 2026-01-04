from typing import Callable

from .creator import Creator
from ..game_loop_controller import GameLoopController

from game_objects.abstract_objects import GameObject, ProcessableObject, ClickableObject

from game_objects.sprites_types import SimpleSprite
from game_objects.map_structure_object import UnitGrid

from ..objects_data import UnitList
from game_objects.map_structure_object import EnemySpawnerGrid, PoliceDeadZone

from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


class MapObjectsCreator(Creator):
    _start_clickable_objects: list[ClickableObject] = None

    _objects: list[ProcessableObject] = None
    _enemies: UnitList = None
    _clickable_objects: list[ClickableObject] = None

    _grid_size: Size = Size()
    _placer: Callable[[None], GameObject] = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        grid_size: Size,
        enemies_patterns: UnitList,
        start_objects: list[GameObject] = (),
        start_clickable_objects: list[GameObject] = (),
    ):
        super().__init__(game_cycle, start_objects)

        self._grid_size = grid_size

        self._start_clickable_objects = start_clickable_objects
        self._clickable_objects = list(start_clickable_objects)

        self._enemies = enemies_patterns

    @property
    def func_placer(self):
        return self._placer

    @func_placer.setter
    def func_placer(self, func: Callable[[None], GameObject]):
        self._placer = func

    def create(self):
        super().create()
        self._clickable_objects.clear()
        self._clickable_objects.extend(list(self._start_clickable_objects))

        unit_grid = self._create_unit_grid(
            SimpleSprite(50, 50, pg.Color(255, 0, 0)),
            SimpleSprite(50, 50, pg.Color(0, 0, 255)),
            Point(100, 225),
        )

        self._clickable_objects.append(unit_grid)

        pos = unit_grid.get_position().copy() + Point(-50 * 4 - 10, 25)

        dead_zone = self._create_dead_zone(pos, False)
        self._objects.append(dead_zone)

        pos = unit_grid.get_positions_of_last_points()[0] + Point(50, 0)
        spawn_grid = self._create_enemy_spawner_grid(pos, Size(3, 5), 10, False)

        self._objects.append(spawn_grid)

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
            position=position,
            depth=-100,
        )

        unit_grid.cell_sprite = cell_sprite
        unit_grid.selected_cell_sprite = selected_cell_s_sprite

        if self._placer is not None:
            unit_grid.on_click_bind(self._placer)

        unit_grid.build()

        return unit_grid

    def _create_dead_zone(self, position: Point, need_render: bool):
        dead_zone = PoliceDeadZone(
            self._game_cycle, SimpleSprite(50 * 4, 50 * 6), position=position
        )

        dead_zone.is_renderable = need_render

        return dead_zone

    def _create_enemy_spawner_grid(
        self,
        position: Point,
        size: Size,
        spawn_interval: int,
        need_render: bool,
    ):
        spawn_grid = EnemySpawnerGrid(
            self._game_cycle.screen,
            SimpleSprite(50, 50, pg.Color(255, 120, 0)),
            size.height,
            size.width,
            self._enemies,
            spawn_interval,
            False,
            position=position,
        )

        spawn_grid.is_renderable = need_render
        spawn_grid.build()

        return spawn_grid

    def get_objects(self):
        return self._objects, self._clickable_objects
