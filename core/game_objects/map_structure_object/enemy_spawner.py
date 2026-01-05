from .spawners_data import UnitList

from ...sprites_types import SimpleSprite

from ..abstract_objects import GameObject


from utility_classes.point import Point

import pygame as pg

import random


class EnemySpawner(GameObject):
    _units: UnitList
    _is_spawn_blocked: bool = False

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        units: UnitList,
        /,
        position: Point = Point(),
        spawn_interval: int = 5,
        is_spawn_blocked: bool = False,
        depth: int = 0,
    ):
        super().__init__(screen, sprite, position=position, depth=depth)

        self._interval = spawn_interval
        self._is_spawn_blocked = is_spawn_blocked

        if type(units) == UnitList:
            self._units = units

        else:
            raise TypeError(f"Unit list must be a UnitList not {type(units)}")

    def set_spawn_block_flag(self, is_blocked: bool):
        self._is_spawn_blocked = is_blocked

    def get_spawn_block_flag(self):
        return self._is_spawn_blocked

    def spawn(self, unit_count: int = 1):
        if unit_count > 0:
            units = self._get_random_unit(unit_count)

            for unit in units:
                unit.set_position(self._position.copy())

            return units

        return ()

    def _get_random_unit(self, count: int):
        return random.choices(self._units, self._units.weights, k=count)
