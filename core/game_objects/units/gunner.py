from .melee import MeleeUnit
from .bullet import Bullet
from .enemy_detector import Detector

from ...sprites_types import SimpleSprite

from utility_classes.point import Point
from utility_classes.size import Size


import pygame as pg


class GunnerUnit(MeleeUnit):
    _type = "gunner"
    _display_name = "Gunner"

    _using_bullet: Bullet = None

    _shoot_interval: int | float = 0
    _shoot_enemy_detector: Detector = None

    _ray_height_indent: int = 0

    _is_can_shoot: bool = True
    _is_shooting: bool = False

    def __init__(
        self,
        *,
        screen: pg.Surface = None,
        sprite: SimpleSprite = None,
        health: int = 100,
        speed: int = 0,
        melee_damage: int = 0,
        bullet: Bullet = None,
        shoot_distance: int | float = 0,
        shoot_interval: int | float = 0,
        team: int = 2,
        position: Point = Point(),
        depth: int = 0,
        price: int = None,
        hit_interval: int = 3,
        hit_distance: int = 1,
        off_melee_detector: bool = False,
        off_shoot_detector: bool = False,
        restricted_objects: list = [],
        ray_height_indent: int = 15,
    ):
        self._using_bullet = bullet
        self._shoot_interval = shoot_interval

        self._off_melee_detector = off_melee_detector
        self._off_shoot_detector = off_shoot_detector

        self._ray_height_indent = ray_height_indent
        self._shoot_distance = shoot_distance

        super().__init__(
            screen=screen,
            sprite=sprite,
            health=health,
            damage=melee_damage,
            speed=speed,
            team=team,
            position=position,
            restricted_objects=restricted_objects,
            depth=depth,
            price=price,
            hit_interval=hit_interval,
            hit_distance=hit_distance,
            ray_height_indent=ray_height_indent,
        )

        self._initialize()

    def _detector_configure(self):
        super()._detector_configure()

        if (
            not self._off_shoot_detector
            and self._sprite is not None
            and self._shoot_enemy_detector is None
        ):
            pos, width, height = self._calculate_ray_pos(
                self._position, self._sprite.rect.width, self._sprite.rect.height
            )

            self._shoot_enemy_detector = Detector(
                screen=self._screen_to_render,
                cell_size=Size(width, height),
                distance=self._shoot_distance,
                position=pos,
            )

            self._shoot_enemy_detector.add_filter(
                lambda game_object: game_object is not None
            )
            self._shoot_enemy_detector.add_filter(
                lambda game_object: not game_object.is_dead()
            )
            self._shoot_enemy_detector.add_filter(
                lambda game_object: issubclass(type(game_object), MeleeUnit)
                and not issubclass(type(game_object), Bullet)
            )

            self._shoot_enemy_detector.refresh()

    def _add_events(self):
        super()._add_events()

        self._events_timer.add(
            "shoot",
            self._shoot_interval,
            lambda delta_time: self._set_shooting(True),
        )

    def _enable_non_timer_attack(self):
        super()._enable_non_timer_attack()

        if not self._events_timer.is_has_event_with_name("shoot"):
            self._is_shooting = True

    @property
    def is_can_shoot(self):
        return self._is_can_shoot

    @is_can_shoot.setter
    def is_can_shoot(self, flag: bool):
        self._is_can_shoot = flag

    def _set_shooting(self, flag: bool):
        self._is_shooting = flag

    def is_detect_far(self, entities: list[MeleeUnit]):
        if self._shoot_enemy_detector is not None:
            if not self._shoot_enemy_detector.can_work:
                self._shoot_enemy_detector.refresh()

            return self._shoot_enemy_detector.is_detect_any(entities)

        return ()

    def shoot(self, damage_modifier: float):
        if not self.is_can_shoot or self._using_bullet is None:
            return

        if self._is_shooting:
            damage = self._using_bullet.get_damage()

            bullet_pos = self._position.copy()
            bullet_pos += self._using_bullet.get_position_offset().copy()

            bullet = self._using_bullet.copy()
            bullet.set_damage(damage * damage_modifier)
            bullet.set_position(bullet_pos)

            if (
                self._events_timer is not None
                and self._events_timer.is_has_event_with_name("shoot")
            ):
                self._is_shooting = False

            return bullet

        return None

    def get_detector(self):
        return self._shoot_enemy_detector

    def destroy(self):
        super().destroy()

        self._shoot_enemy_detector.destroy()

    def set_position(self, position: Point):
        super().set_position(position)

        if self._shoot_enemy_detector is not None:
            pos, _, _ = self._calculate_ray_pos(
                self._position, self._sprite.rect.width, self._sprite.rect.height
            )

            self._shoot_enemy_detector.set_position(pos)

    def __deepcopy__(self, memo: dict[int, MeleeUnit]):
        object_copy = super().__deepcopy__(memo)
        object_copy._using_bullet = self._using_bullet

        object_copy._shoot_interval = self._shoot_interval
        object_copy._shoot_enemy_detector = self._copy_linked_objects(
            self._shoot_enemy_detector
        )

        object_copy._ray_height_indent = self._ray_height_indent

        object_copy._is_can_shoot = self._is_can_shoot
        object_copy._initialize()

        return object_copy
