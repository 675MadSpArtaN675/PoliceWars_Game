from ..abstract_objects import GameObject
from ...sprites_types import SimpleSprite

from .spawners_data import UnitList
from .enemy_spawner import EnemySpawner


from utility_classes.point import Point

from typing import Callable

import random as r

import pygame as pg


class EnemySpawnerLine(GameObject):
    _spawner_list: list[EnemySpawner]
    _units: UnitList

    _spawn_interval: int
    _is_spawn_blocked: bool
    _line_len: int

    @staticmethod
    def units_partition_to_cells(
        spawn_function: Callable[[int, int], list[GameObject]],
        spawning_line_len: int,
        count: int,
        spawn_list: list[GameObject],
    ):
        result = []
        max_count_to_spawn = count

        if len(spawn_list) > 0:
            while max_count_to_spawn > 0:
                random_cage = r.randint(0, spawning_line_len - 1)
                random_count = r.randint(1, max_count_to_spawn)

                result.extend(spawn_function(random_cage, random_count))

                max_count_to_spawn -= random_count

        return result

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        line_len: int,
        units: UnitList,
        spawn_interval: int,
        is_spawn_blocked: bool,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen, sprite, position=position, depth=depth)
        self._spawner_list = []
        self._line_len = line_len
        self._units = units

        self._spawn_interval = spawn_interval
        self._is_spawn_blocked = is_spawn_blocked

    def render(self):
        for cell in self._spawner_list:
            cell.render()

    def build(self):
        pos = self._position.copy()
        for index in range(self._line_len):
            spawner = EnemySpawner(
                self._screen_to_render,
                self._sprite.copy(),
                self._units,
                position=pos.copy(),
                spawn_interval=self._spawn_interval,
                is_spawn_blocked=self._is_spawn_blocked,
                depth=self._depth + index,
            )
            spawner.is_renderable = self.is_renderable

            pos.y += self._sprite.rect.height

            self._spawner_list.append(spawner)

    def spawn(self, count: int):
        return EnemySpawnerLine.units_partition_to_cells(
            self._spawn_unit, self._line_len, count, self._units
        )

    def _spawn_unit(self, cage_number: int, count: int):
        return self._spawner_list[cage_number].spawn(count)

    def __getitem__(self, key: int):
        if key > 0 and key <= self._line_len:
            return self._spawner_list[key - 1]
