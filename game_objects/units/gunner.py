from .melee import MeleeUnit
from .bullet import Bullet
from ..sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class GunnerUnit(MeleeUnit):
    _type = "gunner"
    _display_name = "Gunner"

    _bullet_spawn_position: Point
    _bullet_speed: int

    _bullet_sprite: SimpleSprite = None
    _bullet_type: type

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        bullet_sprite: SimpleSprite,
        health: int,
        speed: int,
        bullet_damage: int,
        bullet_speed: int,
        projectile: type,
        team: int,
        /,
        position: Point = Point(),
        depth: int = 0,
        bullet_spawn_position: Point = Point(),
        restricted_objects: list = [],
    ):
        super().__init__(
            screen,
            sprite,
            health,
            bullet_damage,
            speed,
            team,
            position=position,
            restricted_objects=restricted_objects,
            depth=depth,
        )

        self._bullet_sprite = bullet_sprite
        self._bullet_type = projectile
        self._bullet_spawn_position = bullet_spawn_position.copy()
        self._bullet_speed = bullet_speed

    def attack(self, damage_modifier: float):
        if damage_modifier < 0 or not issubclass(self._bullet_type, Bullet):
            return

        bullet_pos = self._position.copy()
        bullet_pos += self._bullet_spawn_position.copy()

        return self._bullet_type(
            self._screen_to_render,
            self._bullet_sprite.copy(),
            100,
            self._damage * damage_modifier,
            self._bullet_speed,
            position=bullet_pos,
            restricted_objects=[],
        )

    def copy(self):
        object_copy = GunnerUnit(
            self._screen_to_render,
            self._sprite.copy(),
            self._secondary_sprite.copy(),
            self._health,
            self._speed,
            self._damage,
            self._bullet_speed,
            self._bullet_type,
            self._team,
            position=self._position.copy(),
            depth=self._depth,
            bullet_spawn_position=self._bullet_spawn_position,
            restricted_objects=self._restricted_objects,
        )

        self._copy_protected_attrs(object_copy)

        return object_copy
