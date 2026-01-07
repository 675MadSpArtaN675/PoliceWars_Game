from ..abstract_objects import (
    ClickableObject,
    GameObject,
    CollideableObject,
)
from .enemy_detector import Detector
from ...sprites_types import SimpleSprite

from ...event_cores import EventPerformerByTime as PerformerByTime

from utility_classes.point import Point
from utility_classes.size import Size

from typing import Callable

import pygame as pg

DestroyPredicate = Callable[[GameObject], bool]


class MeleeUnit(ClickableObject, CollideableObject):
    _type = "meleeunit"
    _display_name = "MeleeUnit"

    _predicates_to_destroy: list[DestroyPredicate] = ()

    _is_invicible: bool = False
    _is_can_attack: bool = True
    _is_can_move: bool = True

    _is_attacking: bool = False

    _health: int = 0
    _damage: int = 0
    _speed: int = 0

    _team: int = 2

    _hit_interval: int | float = 0
    _hit_distance: int | float = 0

    _melee_detector: Detector = None
    _ray_height_indent: int = 15

    _restricted_objects: list[type] = ()

    _events_timer: PerformerByTime = None

    def __init__(
        self,
        *,
        screen: pg.Surface = None,
        sprite: SimpleSprite = SimpleSprite(50, 50),
        health: int = 100,
        damage: int = 0,
        speed: int = 0,
        team: int = 2,
        position: Point = Point(),
        depth: int = 0,
        hit_interval: int = 3,
        hit_distance: int = 1,
        ray_height_indent: int = 15,
        off_detector: bool = False,
        restricted_objects: list[type] = (),
    ):
        super().__init__(
            screen=screen,
            sprite=sprite,
            secondary_sprite=None,
            position=position.copy(),
            depth=depth,
        )
        self._health = health
        self._damage = damage
        self._speed = speed
        self._hit_interval = hit_interval

        self._restricted_objects = restricted_objects
        self._team = team

        self._predicates_to_destroy = []

        self._events_timer = PerformerByTime()
        self._ray_height_indent = ray_height_indent
        self._hit_distance = hit_distance

        self._off_melee_detector = off_detector

        self.initialize()

    def initialize(self):
        self._detector_configure()
        self.__configure_timer()

    def __configure_timer(self):
        if self._events_timer is not None:
            self._add_events()

        if not self._events_timer.is_has_event_with_name("melee_attack"):
            self._enable_non_timer_attack()

    def _detector_configure(self):
        if not self._off_melee_detector and self._sprite is not None:
            pos, width, height = self._calculate_ray_pos(
                self._position, self._sprite.rect.width, self._sprite.rect.height
            )

            self._melee_detector = Detector(
                self._screen_to_render,
                Size(width, height),
                self._hit_distance,
                position=pos,
            )

        else:
            self._melee_detector = None

    def _add_events(self):
        self._events_timer.add(
            "melee_attack",
            self._hit_interval,
            lambda delta_time: self._set_attack(True),
        )

    def _enable_non_timer_attack(self):
        self._is_attacking = True

    def _calculate_ray_pos(self, sprite_position: Point, width: int, height: int):
        width_, height_ = width, height
        pos = sprite_position.copy()
        pos.x += width
        pos.y += self._ray_height_indent

        height_ -= self._ray_height_indent * 2

        if height_ <= 0:
            height_ = 5

        return pos, width_, height_

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

    def _set_attack(self, value: bool):
        self._is_attacking = value

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

    def event_timer_tick(self, delta_time: int | float):
        if self._events_timer is not None:
            self._events_timer.tick(delta_time)
            self._events_timer.perform_events()

    def add_predicate(self, predicate: DestroyPredicate):
        self._predicates_to_destroy.append(predicate)

    def move(self, delta_time: int | float):
        if self.is_can_move and not self.is_dead():
            now_position = self.get_position()

            distance = self._speed * delta_time
            now_position.x += distance

    def is_detect_melee(self, entities: GameObject):
        return self._is_detect(self._melee_detector, entities)

    def _is_detect(self, detector: Detector, entities: GameObject):
        if self._melee_detector is not None:
            if not detector.can_work:
                detector.refresh()

            return detector.is_detect_any(entities)

        return ()

    def get_damage(self, entity: CollideableObject, damage: float | int):
        if not self.is_invulerable and self._health > 0 and entity is not None:
            self._health -= damage

        return self._health

    def attack(self, entity: GameObject, damage_modificator: float):
        if type(damage_modificator) != float:
            raise TypeError(
                f"Modificator must be a float not {type(damage_modificator)}"
            )

        if self.is_can_attack and self._is_attacking and not self.is_dead():
            damage = self._damage * damage_modificator
            health_remains = entity.get_damage(self, damage)

            if (
                self._events_timer is not None
                and self._events_timer.is_has_event_with_name("melee_attack")
            ):
                self._is_attacking = False

            return True

        return False

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

    def __deepcopy__(self, memo: dict[int, ClickableObject]):
        object_copy = super().__deepcopy__(memo)

        object_copy._predicates_to_destroy = self._predicates_to_destroy

        object_copy._is_invicible = self._is_invicible
        object_copy._is_can_attack = self._is_can_attack
        object_copy._is_can_move = self._is_can_move

        object_copy._health = self._health
        object_copy._damage = self._damage
        object_copy._speed = self._speed
        object_copy._team = self._team
        object_copy._hit_interval = self._hit_interval
        object_copy._hit_distance = self._hit_distance
        object_copy._melee_detector = self._copy_linked_objects(self._melee_detector)

        object_copy._ray_height_indent = self._ray_height_indent
        object_copy._restricted_objects = self._copy_linked_objects(
            self._restricted_objects
        )

        object_copy._events_timer = self._copy_linked_objects(self._events_timer)

        return object_copy
