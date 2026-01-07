from .simple_sprite import SimpleSprite

import pygame as pg
import itertools as it


class AnimatedSprite(SimpleSprite):
    _frame_number: int = 0
    _images: list[pg.Surface] = ()

    def __init__(self, width: int, height: int, images: list[pg.Surface]):
        super().__init__(width, height)

        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and height must be integer")

        if not isinstance(images, list):
            raise TypeError("Images list must be a list")

        if images != [] and images is not None:
            self._images = images
        else:
            raise ValueError("No images in given list!")

    def update(self, *args, **kwargs):
        for frame in it.cycle(self._images):
            frame_transformed = pg.transform.scale(
                frame, (self._rect.width, self._rect.height)
            )

            self._image = frame_transformed
            self._rect = frame_transformed.get_rect()

            yield
