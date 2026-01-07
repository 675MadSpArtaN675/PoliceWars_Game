from .spawners_data import UnitList

from ...sprites_types import SimpleSprite
from ..abstract_objects import GameObject, ProcessableObject


from .enemy_spawner_line import EnemySpawnerLine
from ..units import MeleeUnit


from utility_classes.point import Point

import pygame as pg

import random as r


class EnemySpawnerGrid(GameObject, ProcessableObject):
    _spawner_list: list[EnemySpawnerLine] = None
    _units: UnitList = None

    _spawn_interval: int = 0

    _line_count: int = 0
    _line_len: int = 0

    _is_spawn_blocked: bool = False

    def __init__(
        self,
        *,
        screen: pg.Surface,
        sprite: SimpleSprite,
        line_len: int,
        line_count: int,
        units: UnitList,
        spawn_interval: int,
        is_spawn_blocked: bool,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(screen=screen, sprite=sprite, position=position, depth=depth)

        self._spawner_list = []

        self._line_count = line_count
        self._line_len = line_len

        self._units = units

        self._spawn_interval = spawn_interval
        self._is_spawn_blocked = is_spawn_blocked

    def render(self):
        for line in self._spawner_list:
            line.render()

    def process(self, delta_time: int | float, **kwargs):
        if not self._is_spawn_blocked and self._time >= self._spawn_interval:
            enemies: list[MeleeUnit] = kwargs.get("enemies")

            if enemies is not None:
                spawned_enemies = self.spawn(10)
                enemies.extend(spawned_enemies)

            self._time = 0
            return

        self._time += delta_time

    def build(self):
        pos = self._position.copy()

        for index in range(self._line_count):
            spawner = EnemySpawnerLine(
                screen=self._screen_to_render,
                sprite=self._sprite.copy(),
                line_len=self._line_len,
                units=self._units,
                spawn_interval=self._spawn_interval,
                is_spawn_blocked=self._is_spawn_blocked,
                position=pos.copy(),
                depth=self._depth + index,
            )
            spawner.is_renderable = self.is_renderable

            spawner.build()

            self._spawner_list.append(spawner)
            pos.x += self._sprite.rect.width

    def spawn(self, count: int):
        return EnemySpawnerLine.units_partition_to_cells(
            self._spawn_unit, self._line_count, count, self._units
        )

    def _spawn_unit(self, cage_number: int, count: int):
        return self._spawner_list[cage_number].spawn(count)

    def __getitem__(self, key: int):
        if type(key) == int:
            if key > 0 and key <= self._line_count:
                return self._spawner_list[key - 1]

        elif type(key) == tuple and len(key) > 1:
            first_key = key[0]
            second_key = key[1]

            if first_key > 0 and first_key <= self._line_count:
                line = self._spawner_list[first_key - 1]

                if second_key > 0 and second_key <= self._line_len:
                    return line[second_key]

        raise IndexError("Incorrect index")

    def __deepcopy__(self, memo: dict[int, GameObject]):
        object_copy = super().__deepcopy__(memo)

        object_copy._spawner_list = self._spawner_list.copy()
        object_copy._units = self._units

        object_copy._spawn_interval = self._spawn_interval
        object_copy._is_spawn_blocked = self._is_spawn_blocked

        object_copy._line_len = self._line_len
        object_copy._line_count = self._line_count

        self._copy(object_copy, self._interval)

        return object_copy
