from ...sprites_types import SimpleSprite
from ..abstract_objects import GameObject

from utility_classes.size import Size
from utility_classes.point import Point

from typing import Callable

from copy import deepcopy

import pygame as pg

Predicate = Callable[[GameObject], bool]


class Detector(GameObject):
    _detected_entities: list[GameObject] = None

    _cell_size: Size = None
    _detection_distance: int | float = None
    _ignore_units: list[str] = None

    _filters: list[Predicate] = None

    def __init__(
        self,
        screen: pg.Surface = None,
        cell_size: Size = Size(),
        distance: int | float = 0,
        position: Point = Point(),
        ignore_units: list[str] = (),
        depth: int = 0,
    ):
        super().__init__(screen=screen, sprite=None, position=position, depth=depth)

        self._cell_size = cell_size
        self._detection_distance = distance
        self._ignore_units = ignore_units
        self._filters = []
        self._detected_entities = ()

    @property
    def can_work(self):
        return self._sprite is not None

    def add_filter(self, function: Predicate):
        if function is not None:
            self._filters.append(function)

    def remove_filter(self, function: Predicate):
        if function is not None:
            self._filters.remove(function)

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

    def detect_any(self, entities: list[GameObject]):
        if self._sprite is not None:
            filtered_entities = self._filter_entities(entities)

            if len(filtered_entities) > 0:
                ents = tuple(map(lambda x: x.get_sprite().rect, filtered_entities))

                collided_entities = self._sprite.rect.collideobjects(ents)

                if collided_entities is not None and len(collided_entities) > 0:
                    self._detected_entities = collided_entities
                    return collided_entities

        return ()

    def detect(self, entity: GameObject):
        return self.detect_any([entity])

    def is_detect_any(self, entities: list[GameObject]):
        return len(self.detect_any(entities)) > 0

    def is_detect(self, entity: GameObject):
        return len(self.is_detect_any([entity])) > 0

    def is_empty(self):
        return len(self._detected_entities) <= 0

    def clear_buffer(self):
        if len(self._detected_entities) > 0:
            self._detected_entities.clear()

    def _filter_entities(self, entities: list[GameObject]):
        if len(self._filters) <= 0:
            return entities

        result = []
        for entity in entities:
            answer = [filter_func(entity) for filter_func in self._filters]

            if all(answer):
                result.append(entity)

        return tuple(result)

    def __deepcopy__(self, memo: dict[int, GameObject]):
        object_copy = super().__deepcopy__(memo)

        object_copy._detected_entities = []

        object_copy._cell_size = deepcopy(self._cell_size)
        object_copy._detection_distance = self._detection_distance

        object_copy._ignore_units = self._ignore_units
        object_copy._filters = self._filters

        return object_copy
