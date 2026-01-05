from .gunner import MeleeUnit

from ...sprites_types import SimpleSprite
from ..abstract_objects import GameObject

from utility_classes.size import Size
from utility_classes.point import Point

import pygame as pg


class Detector(GameObject):
    _detected_entities: list[MeleeUnit]

    _cell_size: Size
    _detection_distance: int | float
    _ignore_units: list[str]

    def __init__(
        self,
        screen: pg.Surface,
        cell_size: Size,
        distance: int | float,
        position: Point = Point(),
        ignore_units: list[str] = (),
    ):
        super().__init__(screen, None, position, 0)

        cell_size.height *= 0.8
        self._cell_size = cell_size
        self._detection_distance = distance
        self._ignore_units = ignore_units

    @property
    def can_work(self):
        return self._sprite is not None

    def refresh(self):
        self._sprite = SimpleSprite(
            self._cell_size.width * self._detection_distance,
            self._cell_size.height,
            pg.Color(255, 255, 255),
        )
        self._sprite.rect.x = self._position.x
        self._sprite.rect.y = self._position.y

    def get_distance(self):
        return self._detection_distance

    def set_distance(self, value: float | int):
        self._detection_distance = value

    def detect_any(self, entities: list[MeleeUnit]):
        if self._sprite is not None:
            filtered_entities = filter(
                lambda x: issubclass(type(x), MeleeUnit),
                entities,
            )

            ents = tuple(map(lambda x: x.get_sprite().rect, filtered_entities))

            collided_entities = self._sprite.rect.collideobjects(ents)

            if collided_entities is not None and len(collided_entities) > 0:
                self._detected_entities = collided_entities
                return collided_entities

        return ()

    def detect(self, entity: MeleeUnit):
        return self.detect_any([entity])

    def is_detect_any(self, entities: list[MeleeUnit]):
        return len(self.detect_any(entities)) > 0

    def is_detect(self, entity: MeleeUnit):
        return len(self.is_detect_any([entity])) > 0

    def clear_buffer(self):
        if self._detected_entities != () and self._detected_entities != []:
            self._detected_entities = ()

    def copy(self):
        object_copy = Detector(
            self._screen_to_render,
            self._cell_size.copy(),
            self._detection_distance,
            position=self._position.copy(),
            ignore_units=self._ignore_units,
        )

        self._copy_protected_attrs(object_copy)

    def _copy_protected_attrs(self, object_copy: GameObject):
        super()._copy_protected_attrs(object_copy)
