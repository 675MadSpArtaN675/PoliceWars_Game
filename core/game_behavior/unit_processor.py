from .game_loop_controller import GameLoopController

from ..game_objects.units import MeleeUnit, GunnerUnit, Bullet

from .unit_control import UnitChooser


class UnitProcessor:
    _game_cycle: GameLoopController

    _chooser: UnitChooser

    _policemans: list[MeleeUnit]
    _bullets: list[Bullet]

    def __init__(
        self,
        game_cycle: GameLoopController,
        chooser: UnitChooser,
        policemans: list[MeleeUnit],
        bullets: list[Bullet],
    ):
        self._game_cycle = game_cycle

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
            unit.event_timer_tick(delta_time)

            objects_to_collide_list = self._union_list(objects_to_collide_list)

            if unit.health <= 0.0 and not unit.is_invulerable:
                unit.killself()

            collide = self._collide_with_accessed_objects(unit, objects_to_collide_list)

            if not collide and unit.is_can_move:
                unit.move(delta_time)

            self._gunner_shoot(unit, objects_to_collide_list, collide)

    def _gunner_shoot(
        self,
        unit: GunnerUnit,
        objects_to_collide_list: list[MeleeUnit | GunnerUnit],
        collide: bool,
    ):
        if issubclass(type(unit), GunnerUnit):
            if (
                not collide
                and not unit.is_detect_melee(objects_to_collide_list)
                and unit.is_detect_far(objects_to_collide_list)
            ):
                shoot_bullet = unit.shoot(1.0)

                if shoot_bullet is not None:
                    self._bullets.append(shoot_bullet)

    def _collide_with_accessed_objects(
        self, unit: MeleeUnit, objects_to_collide_list: list[MeleeUnit]
    ):
        collide = False
        for object_to_collide in objects_to_collide_list:
            is_objects_collide = unit.collision(object_to_collide)
            if (
                object_to_collide is not None
                and not object_to_collide.is_dead()
                and object_to_collide.team != unit.team
                and is_objects_collide
            ):
                if is_objects_collide or unit.is_detect_melee(objects_to_collide_list):
                    unit.attack(object_to_collide, 1.0)

                collide = True
                break

        return collide

    def _union_list(self, objects: list[list[MeleeUnit]]):
        result = []
        for object_ in objects:
            result.extend(object_)

        return tuple(result)

    def police_place(self):
        if (
            not self._game_cycle.is_paused()
            and not self._game_cycle.is_delete_mode_activated()
        ):
            unit = self._chooser.extract_unit()

            if unit is not None:
                self._policemans.append(unit)

                return unit, False

        elif (
            not self._game_cycle.is_paused()
            and self._game_cycle.is_delete_mode_activated()
        ):
            return None, True

        return None, False
