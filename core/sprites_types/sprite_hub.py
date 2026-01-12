from .sprite_base import SpriteBase
from .simple_sprite import SimpleSprite

from utility_classes import Point, Size

import pygame as pg


class SpriteHub(SpriteBase):
    _screen: pg.Surface = None
    _position: Point = None

    _states: dict[str, SimpleSprite] = dict()

    def __init__(
        self,
        screen: pg.Surface,
        size: Size,
        states: dict[str, SimpleSprite] = None,
        position: Point = Point(),
    ):
        super().__init__(*size.to_tuple(), position=position, is_alpha=True)

        if states is not None:
            self._states = states

        self._screen = screen
        self._position = position

    def update(self, *args, **kwargs):
        state_name = kwargs.get("state", None)

        if state_name is not None:
            state = self._states[state_name]

            state.rect.x, state.rect.y = self._position.to_tuple()
            state.update()

            self._image = state.image
            self._rect = state.rect

    def add_state(self, state_name: str, sprite: SimpleSprite):
        if len(state_name) > 0 and sprite is not None:
            self._states[state_name] = sprite

    def remove_state(self, state_name: str):
        state = self._states.get(state_name)

        if state is not None:
            del self._states[state_name]

    def copy(self):
        object_copy = super().copy()

        object_copy._states = self._states.copy()
        object_copy._position = self._position.copy()

        return object_copy
