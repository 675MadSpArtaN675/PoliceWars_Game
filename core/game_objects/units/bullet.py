from ..abstract_objects import GameObject

from ...sprites_types import SimpleSprite
from .melee import MeleeUnit

from utility_classes.point import Point

from dataclasses import dataclass
from copy import deepcopy

import pygame as pg


@dataclass
class BulletData:
    health: float
    speed: float
    damage: float

    bullet_spawn_offset: Point

    def __deepcopy__(self):
        return BulletData(
            self.health, self.speed, self.damage, self.bullet_spawn_offset.copy()
        )


class Bullet(MeleeUnit):
    _type = "projectile"
    _display_name = "Bullet"

    _bullet_data: BulletData = None

    def __init__(
        self,
        *,
        screen: pg.Surface = None,
        sprite: SimpleSprite = None,
        bullet_data: BulletData = None,
        team: int = 2,
        position: Point = Point(),
        restricted_objects=(),
        depth: int = 0,
    ):
        super().__init__(
            screen=screen,
            sprite=sprite,
            health=bullet_data.health,
            damage=bullet_data.damage,
            speed=bullet_data.speed,
            team=team,
            position=position,
            restricted_objects=restricted_objects,
            depth=depth,
            off_detector=True,
        )

        self._bullet_data = bullet_data
        self._is_ghost_object = True

    def _add_events(self):
        pass

    def set_health(self, health: int | float):
        self._bullet_data.health = health

    def set_damage(self, damage: int | float):
        self._bullet_data.damage = damage

    def set_speed(self, speed: int | float):
        self._bullet_data.speed = speed

    def get_health(self):
        return self._bullet_data.health

    def get_damage(self):
        return self._bullet_data.damage

    def get_speed(self):
        return self._bullet_data.speed

    def attack(self, entity: GameObject, damage_modificator: float):
        if super().attack(entity, damage_modificator):
            self.killself()

    def __deepcopy__(self, memo):
        object_copy = super().__deepcopy__(memo)

        object_copy._bullet_data = deepcopy(self._bullet_data)

        return object_copy
