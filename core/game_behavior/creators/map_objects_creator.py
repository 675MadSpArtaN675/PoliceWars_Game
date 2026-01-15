from ...sprites_types import SpriteBase, SimpleSprite

from .. import GameLoopController

from ...game_objects.abstract_objects import (
    GameObject,
    ProcessableObject,
    ClickableObject,
)
from ...game_objects.map_structure_object import (
    UnitGrid,
    EnemySpawnerGrid,
    PoliceDeadZone,
)
from ...game_objects.map_structure_object.spawners_data import UnitList

from .creator import Creator

from utility_classes.point import Point
from utility_classes.size import Size

from typing import Callable

import pygame as pg


class MapObjectsCreator(Creator):
    category: str = "map_object_texture"
    _start_clickable_objects: list[ClickableObject] = None

    _objects: list[ProcessableObject] = None
    _enemies: UnitList = None
    _clickable_objects: list[ClickableObject] = None

    _grid_size: Size = Size()
    _placer: Callable[[None], GameObject] = None

    debug_mode: bool = False
    cell_size: Size = Size(64, 64)
    unit_grid_position: Point = Point()
    distance_in_cells_count: int = 1

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

        width, height = self.cell_size.to_tuple()

        unit_grid = self._create_unit_grid(
            self._get_texture("unit_cell", "base"),
            self._get_texture("selected_unit_cell", "select"),
            self.unit_grid_position.copy(),
        )

        self._clickable_objects.append(unit_grid)

        pos = self.unit_grid_position.copy() + Point(-width * 5, 25)

        dead_zone = self._create_dead_zone(
            SimpleSprite(width * 4, height * 6), pos, self.debug_mode
        )
        self._objects.append(dead_zone)

        pos_d = Point(width * self.distance_in_cells_count, 0)
        pos = unit_grid.get_positions_of_last_points()[0] + pos_d

        spawn_grid = self._create_enemy_spawner_grid(
            SimpleSprite(width, height, pg.Color(255, 120, 0)),
            pos,
            Size(3, 5),
            15,
            self.debug_mode,
        )

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
            screen=self._game_cycle.screen,
            rows=self._grid_size.width,
            columns=self._grid_size.height,
            position=position.copy(),
            depth=-100,
        )

        unit_grid.cell_sprite = cell_sprite
        unit_grid.selected_cell_sprite = selected_cell_s_sprite

        if self._placer is not None:
            unit_grid.on_click_bind(self._placer)

        unit_grid.build()

        return unit_grid

    def _create_dead_zone(self, sprite: SpriteBase, position: Point, need_render: bool):

        dead_zone = PoliceDeadZone(
            game_cycle=self._game_cycle,
            sprite=sprite,
            position=position,
        )

        dead_zone.is_renderable = need_render

        return dead_zone

    def _create_enemy_spawner_grid(
        self,
        sprite: SpriteBase,
        position: Point,
        size: Size,
        spawn_interval: int,
        need_render: bool,
    ):
        spawn_grid = EnemySpawnerGrid(
            screen=self._game_cycle.screen,
            sprite=sprite,
            line_len=size.height,
            line_count=size.width,
            units=self._enemies,
            spawn_interval=spawn_interval,
            is_spawn_blocked=False,
            position=position,
        )

        spawn_grid.is_renderable = need_render
        spawn_grid.build()

        return spawn_grid

    def get_objects(self):
        return self._objects, self._clickable_objects
