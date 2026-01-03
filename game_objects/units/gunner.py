from .melee import MeleeUnit
from .bullet import Bullet
from .enemy_detector import Detector
from ..sprites_types import SimpleSprite

from dataclasses import dataclass
from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


@dataclass
class BulletData:
    shoot_interval: int | float
    bullet_spawn_position: Point
    bullet_speed: int

    bullet_sprite: SimpleSprite = None
    bullet_type: type = None


class GunnerUnit(MeleeUnit):
    _type = "gunner"
    _display_name = "Gunner"

    _bullet_settings: BulletData = None
    _enemy_detector: Detector = None

    _is_show_detector_distance: bool = False
    _ray_height_indent: int = 0

    _time_to_shoot: int = 0

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
        shoot_distance: int | float,
        shoot_interval: int | float,
        team: int,
        /,
        position: Point = Point(),
        depth: int = 0,
        bullet_spawn_position: Point = Point(),
        restricted_objects: list = [],
        show_detector: bool = False,
        distance_ray_height_indent: int = 15,
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

        self._bullet_settings = BulletData(
            shoot_interval,
            bullet_spawn_position.copy(),
            bullet_speed,
            bullet_sprite,
            projectile,
        )

        self._ray_height_indent = distance_ray_height_indent

        pos, width, height = self._calculate_ray_pos(
            self._position, self._sprite.rect.width, self._sprite.rect.height
        )

        self._enemy_detector = Detector(
            screen, Size(width, height), shoot_distance, position=pos
        )
        self._enemy_detector.refresh()

        self._is_show_detector_distance = show_detector

    def _calculate_ray_pos(self, sprite_position: Point, width: int, height: int):
        width_, height_ = width, height
        pos = sprite_position.copy()
        pos.y += self._ray_height_indent

        return pos, width_, height_

    @property
    def IsNeedToShowDetector(self):
        return self._is_show_detector_distance

    @IsNeedToShowDetector.setter
    def IsNeedToShowDetector(self, flag: bool):
        self._is_show_detector_distance = flag

    def render_detector(self):
        if self._is_show_detector_distance:
            self._enemy_detector.render()

    def is_detect(self, entities: list[MeleeUnit]):
        if not self._enemy_detector.can_work:
            self._enemy_detector.refresh()

        return self._enemy_detector.is_detect_any(entities)

    def shoot(self, damage_modifier: float, delta_time: int):
        if self._time_to_shoot >= self._bullet_settings.shoot_interval:
            if (
                self.is_can_attack
                and damage_modifier < 0
                or not issubclass(self._bullet_settings.bullet_type, Bullet)
            ):
                return

            bullet_pos = self._position.copy()
            bullet_pos += self._bullet_settings.bullet_spawn_position.copy()

            bullet = self._bullet_settings.bullet_type(
                self._screen_to_render,
                self._bullet_settings.bullet_sprite.copy(),
                100,
                self._damage * damage_modifier,
                self._bullet_settings.bullet_speed,
                self._team,
                position=bullet_pos,
                restricted_objects=[],
            )

            self._time_to_shoot = 0
            return bullet

        self._time_to_shoot += delta_time
        return None

    def set_position(self, position):
        super().set_position(position)

        pos, _, _ = self._calculate_ray_pos(
            self._position, self._sprite.rect.width, self._sprite.rect.height
        )

        self._enemy_detector.set_position(pos)

    def copy(self):
        object_copy = GunnerUnit(
            self._screen_to_render,
            self._sprite.copy(),
            self._secondary_sprite.copy(),
            self._health,
            self._speed,
            self._damage,
            self._bullet_settings.bullet_speed,
            self._bullet_settings.bullet_type,
            self._enemy_detector.get_distance(),
            self._bullet_settings.shoot_interval,
            self._team,
            position=self._position.copy(),
            depth=self._depth,
            bullet_spawn_position=self._bullet_settings.bullet_spawn_position,
            restricted_objects=self._restricted_objects,
            show_detector=self._is_show_detector_distance,
            distance_ray_height_indent=self._ray_height_indent,
        )

        self._copy_protected_attrs(object_copy)

        return object_copy
