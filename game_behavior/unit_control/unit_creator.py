from game_objects.units import MeleeUnit, GunnerUnit

from ..objects_data import UnitData, UnitType

import pygame as pg


class UnitCreator:
    _screen_on_create: pg.Surface = None

    def __init__(self, screen: pg.Surface):
        self._screen_on_create = screen

    def create_unit_by_type(
        self, unit_type: type, projectile: type, unit_data: UnitData
    ):
        if not (isinstance(unit_data, UnitData) or issubclass(unit_data, UnitData)):
            raise NotImplementedError("No required dataclass for create unit")

        match (unit_data.unit_type):
            case UnitType.Melee:
                return self._create_melee_unit(unit_type, unit_data)

            case UnitType.Gunner:
                return self._create_gunner_unit(unit_type, projectile, unit_data)

            case _:
                raise NotImplementedError("Given type of unit not exists.")

    def _create_melee_unit(self, unit_type: type, unit_data: UnitData):
        if MeleeUnit in unit_type.__mro__:
            return unit_type(
                self._screen_on_create,
                unit_data.textures["primary_sprite"],
                unit_data.health,
                unit_data.damage,
                unit_data.speed,
                position=unit_data.position,
                depth=unit_data.depth,
            )

    def _create_gunner_unit(
        self, unit_type: type, projectile: type, unit_data: UnitData
    ):
        if GunnerUnit in unit_type.__mro__:
            return unit_type(
                self._screen_on_create,
                unit_data.textures["primary_sprite"],
                unit_data.textures["bullet_sprite"],
                unit_data.health,
                unit_data.speed,
                unit_data.damage,
                unit_data.bullet_speed,
                projectile,
                position=unit_data.position,
                depth=unit_data.depth,
                bullet_spawn_position=unit_data.bullet_spawn_position,
            )
