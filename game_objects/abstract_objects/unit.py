from ..abstract_objects import ClickableObject, GameObject
from ..abstract_objects.sprites_types import SimpleSprite

from utility_classes.point import Point

import pygame as pg


class Unit(ClickableObject):
    _type = "unit"
    _display_name = "Unit"

    _is_invicible: bool = False

    _health: int
    _damage: int
    _speed: int

    _restricted_objects: list[type]

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        /,
        position: Point = Point(),
        depth: int = 0,
        restricted_objects: list[type] = [],
    ):
        super().__init__(screen, sprite, None, position=position.copy(), depth=depth)
        self._health = health
        self._damage = damage
        self._speed = speed

        self._restricted_objects = restricted_objects

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
        if type(entity) in self._restricted_objects:
            return False

        sprite = self.get_sprite()
        sprite_enemy = entity.get_sprite()

        return pg.sprite.collide_rect(sprite, sprite_enemy)

    def attack(self, entity: GameObject, damage):
        is_collision = self.collision(entity)
        if is_collision:
            health_remains = entity.get_damage(self, self._damage)

        return is_collision

    @property
    def is_invicible(self):
        return self._is_invicible

    @is_invicible.setter
    def is_invicible(self):
        return self._is_invicible
