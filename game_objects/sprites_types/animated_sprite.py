from simple_sprite import SimpleSprite

import pygame as pg
import itertools as it


class AnimatedSprite(SimpleSprite):
    _frame_number: int
    _images: list[pg.Surface]

    def __init__(self, width: int, height: int, images: list[str]):
        super().__init__(width, height)

        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Width and height must be integer")

        if not isinstance(images, list):
            raise TypeError("Images list must be a list")

        if images != []:
            self._images = [
                pg.image.load(image_path)
                for image_path in images
                if image_path != "" and image_path is not None
            ]

    def update(self, *args, **kwargs):
        for frame in it.cycle(self._images):
            frame_transformed = pg.transform.scale(
                frame, (self._rect.width, self._rect.height)
            )

            self._image = frame_transformed
            self._rect = frame_transformed.get_rect()

            yield
