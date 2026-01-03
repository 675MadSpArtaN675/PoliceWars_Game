from ..abstract_objects import GameObject
from ..sprites_types import SimpleSprite

from .enemy_spawner import EnemySpawner
from game_behavior.objects_data import UnitList

from utility_classes.point import Point

import random as r

import pygame as pg


class EnemySpawnerLine(GameObject):
    _spawner_list: list[EnemySpawner]
    _units: UnitList

    _spawn_interval: int
    _is_spawn_blocked: bool
    _line_len: int

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

    def init_line(self):
        pos = self._position.copy()
        for index in range(self._line_len):
            spawner = EnemySpawner(
                self._screen_to_render,
                self._sprite,
                self._units,
                position=pos,
                spawn_interval=self._spawn_interval,
                is_spawn_blocked=self._is_spawn_blocked,
                depth=self._depth + index,
            )

            self._spawner_list.append(spawner)

        return

    def spawn(self, count: int):
        result = []

        if len(self._spawner_list) > 0:
            for _ in range(count):
                spawner_num = r.randint(0, self._line_len)

                result.append(self._spawner_list[spawner_num])

        return result

    def __getitem__(self, key: int):
        if key > 0 and key <= self._line_len:
            return self._spawner_list[key - 1]
