from game_behavior.unit_control import UnitChooser
from game_objects.units import MeleeUnit, GunnerUnit, Bullet

import pygame as pg


class UnitProcessor:
    _chooser: UnitChooser

    _policemans: list[MeleeUnit]
    _bullets: list[Bullet]

    def __init__(
        self, chooser: UnitChooser, policemans: list[MeleeUnit], bullets: list[Bullet]
    ):
        self._chooser = chooser
        self._policemans = policemans
        self._bullets = bullets

    def process(
        self,
        unit: MeleeUnit | GunnerUnit,
        delta_time: int | float,
        objects_to_collide_list: list[list[MeleeUnit | GunnerUnit]],
    ):
        if unit is not None and type(unit) not in (tuple, list):
            objects_to_collide_list = self._union_list(objects_to_collide_list)

            if unit.health <= 0:
                unit.destroy()

            collide = self._collide_with_accessed_objects(unit, objects_to_collide_list)

            if not collide and unit.is_can_move:
                unit.move(delta_time)

            if issubclass(type(unit), Bullet) and collide:
                unit.destroy()
                return

            self._gunner_shoot(unit, delta_time, objects_to_collide_list, collide)

    def _gunner_shoot(self, unit, delta_time, objects_to_collide_list, collide):
        if issubclass(type(unit), GunnerUnit):
            if (
                unit.is_can_attack
                and not collide
                and unit.is_detect(objects_to_collide_list)
            ):
                shoot_bullet = unit.shoot(1.0, delta_time)

                if shoot_bullet is not None:
                    self._bullets.append(shoot_bullet)

    def _collide_with_accessed_objects(self, unit, objects_to_collide_list):
        collide = False
        for object_to_collide in objects_to_collide_list:
            if (
                object_to_collide is not None
                and not object_to_collide.is_dead()
                and object_to_collide.team != unit.team
                and unit.collision(object_to_collide)
            ):
                unit.attack(object_to_collide, 1.0)

                if object_to_collide.health < 1:
                    object_to_collide.destroy()

                collide = True
                break
        return collide

    def _union_list(self, objects: list[list[MeleeUnit]]):
        result = []
        for object_ in objects:
            result.extend(object_)

        return tuple(result)

    def police_place(self):
        unit = self._chooser.extract_unit()
        self._policemans.append(unit)

        return unit
