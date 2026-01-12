from .simple_sprite import SimpleSprite
from .data import ImageOptions

import pygame as pg


class Animator(SimpleSprite):
    _interval_between_frames: int | float = 0
    _time: int | float = 0

    _frame_number: int = 0
    _max_frames: int = 0
    _images: list[pg.Surface] = ()

    def __init__(
        self,
        width: int,
        height: int,
        interval_between_frames: int | float,
        images_configs: list[ImageOptions],
    ):
        super().__init__(width, height, is_alpha=True)

        if type(images_configs) not in (tuple, list):
            raise TypeError("No list or tuple of configs")

        self._images = images_configs
        self._max_frames = len(self._images)
        self._interval_between_frames = interval_between_frames

    def update(self, *args, **kwargs):
        if self._frame_number > 0 and len(self._images) > 0:
            self._data = self._next_frame(kwargs.get("delta_time", 0))

        super().update()

    def _next_frame(self, delta_time: int):
        if self._time >= self._interval_between_frames:
            if self._frame_number < self._max_frames:
                self._data = self._images[self._frame_number]
            else:
                self._data = self._images[0]

        self._time += delta_time

        return self._data
