from game_objects.abstract_objects import GameObject, ClickableObject
from .objects_data import ObjectData, ClickableObjectData

import pygame as pg


class ObjectCreator:
    _screen_to_render: pg.Surface = None

    def __init__(self, screen: pg.Surface):
        self._screen_to_render = screen

    def create(self, object_data: ObjectData | ClickableObjectData):
        if isinstance(object_data, ObjectData):
            return
        elif isinstance(object_data, ClickableObjectData):
            return

    def _create_object(self, data: ObjectData):
        return GameObject(
            self._screen_to_render,
            data.sprite.copy(),
            position=data.position.copy(),
            depth=data.depth.copy(),
        )

    def _create_clickable_object(self, data: ClickableObjectData):
        return ClickableObject(
            self._screen_to_render,
            data.primary_sprite.copy(),
            data.secondary_sprite.copy(),
            position=data.position.copy(),
        )
