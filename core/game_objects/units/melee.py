from ..abstract_objects import (
    ClickableObject,
    GameObject,
    CollideableObject,
)
from ...sprites_types import SimpleSprite

from utility_classes.point import Point

from typing import Callable

import pygame as pg


DestroyPredicate = Callable[[GameObject], bool]


class MeleeUnit(ClickableObject, CollideableObject):
    _type = "meleeunit"
    _display_name = "MeleeUnit"

    _predicates_to_destroy: list[DestroyPredicate] = None

    _is_invicible: bool = False
    _is_can_attack: bool = True
    _is_can_move: bool = True

    _health: int
    _damage: int
    _speed: int

    _restricted_objects: list[type]

    _time_to_hit: int | float = 0

    def __init__(
        self,
        screen: pg.Surface,
        sprite: SimpleSprite,
        health: int,
        damage: int,
        speed: int,
        team: int,
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
        self._team = team

        self._predicates_to_destroy = []

    @property
    def is_can_move(self):
        return self._is_can_move

    @is_can_move.setter
    def is_can_move(self, value: bool):
        self._is_can_move = value

    @property
    def is_can_attack(self):
        return self._is_can_attack

    @is_can_attack.setter
    def is_can_attack(self, value: bool):
        self._is_can_attack = value

    @property
    def is_invulerable(self):
        return self._is_invicible

    @is_invulerable.setter
    def is_invulerable(self, value: bool):
        self._is_invicible = value

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team: int):
        self._team = team

    @property
    def health(self):
        return self._health

    @property
    def self_destruction_predicates(self):
        return self._predicates_to_destroy

    @self_destruction_predicates.setter
    def self_destruction_predicates(
        self,
        predicates: DestroyPredicate | tuple[DestroyPredicate] | list[DestroyPredicate],
    ):
        if type(predicates) in [tuple, list]:
            self._predicates_to_destroy.extend(predicates)

        else:
            self._predicates_to_destroy.append(predicates)

    def add_predicate(self, predicate: DestroyPredicate):
        self._predicates_to_destroy.append(predicate)

    def move(self, delta_time: int | float):
        if self.is_can_move and not self.is_dead():
            now_position = self.get_position()

            distance = self._speed * delta_time
            now_position.x += distance

    def get_damage(self, entity, damage):
        if not self.is_invulerable and self._health > 0 and entity is not None:
            self._health -= damage

        return self._health

    def attack(self, entity: GameObject, damage_modificator: float):
        if type(damage_modificator) != float:
            raise TypeError(
                f"Modificator must be a float not {type(damage_modificator)}"
            )

        is_collision = self.collision(entity)
        if self.is_can_attack and not self.is_dead() and is_collision:
            health_remains = entity.get_damage(self, self._damage * damage_modificator)

        return is_collision

    def killself(self):
        if (
            self._predicates_to_destroy is not None
            and len(self._predicates_to_destroy) > 0
        ):
            need_destroy = any(
                [predicate(self) for predicate in self._predicates_to_destroy]
            )

            if not need_destroy:
                return

        self.destroy()

    def copy(self):
        object_copy = MeleeUnit(
            self._screen_to_render,
            self._sprite.copy(),
            self._health,
            self._damage,
            self._speed,
            self._team,
            position=self._position.copy(),
            depth=self._depth,
            restricted_objects=self._restricted_objects,
        )

        self._copy_protected_attrs(object_copy)

        return object_copy

    def _copy_protected_attrs(self, object_copy: object):
        super()._copy_protected_attrs(object_copy)
        attrs = ["_is_invicible", "_is_can_attack", "_is_can_move"]

        for attribute in attrs:
            self_attr_value = getattr(self, attribute)
            setattr(object_copy, attribute, self_attr_value)
