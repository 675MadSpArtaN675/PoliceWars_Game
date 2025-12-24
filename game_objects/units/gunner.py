from ..abstract_objects import Unit, Bullet
from ..abstract_objects.sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class GunnerUnit(Unit):
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
        bullet_damage: int,
        speed: int,
        bullet_speed: int,
        projectile: type,
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
            restricted_objects=[PoliceUnit],
        )
