from .abstract_objects import ClickableObject, GameObject
from .abstract_objects.sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class Unit(ClickableObject):
    _is_invicible: bool = False

    _health: int
    _damage: int
    _speed: int

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        /,
        position: Point = Point(),
    ):
        super().__init__(screen, sprite, None, position=position)
        self._health = health
        self._damage = damage
        self._speed = speed

    @property
    def health(self):
        return self._health

    def move(self, delta_time):
        now_position = self.get_position()

        distance = self._speed * delta_time
        now_position.x += distance

    def get_damage(self, entity, damage):
        if not self.is_invicible and self._health > 0 and entity is not None:
            self._health -= damage

        return self._health

    def collision(self, entity: GameObject):
        return pg.sprite.collide_rect(self.get_sprite(), entity.get_sprite())

    def attack(self, entity: GameObject, damage):
        health_remains = entity.get_damage(self, damage)

    @property
    def is_invicible(self):
        return self._is_invicible

    @is_invicible.setter
    def is_invicible(self):
        return self._is_invicible


class BanditUnit(Unit):
    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        /,
        position: Point = Point(),
    ):
        super().__init__(screen, sprite, health, damage, speed, position=position)


class Bullet(Unit):
    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        /,
        position: Point = Point(),
    ):
        super().__init__(screen, sprite, health, damage, speed, position=position)


class PoliceUnit(GameObject):
    _health: int
    _damage: int

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        /,
        position: Point = Point(),
    ):
        super().__init__(screen, sprite, position=position)

        self._health = health
        self._damage = damage
