from utility_classes import Size, Point

from dataclasses import dataclass

from .enum import SpriteType, FlipSide

import pygame as pg


@dataclass
class ImageOptions:
    category: str
    file_name: str
    name: str

    sprite_type: SpriteType
    flip: FlipSide

    scale: Size
    position: Point

    frame_num: int = None

    def set_image(self, image: pg.Surface):
        self._image = image

    def get_image(self):
        image = getattr(self, "_image", None)

        if image is not None:
            return image

    def get_frame_num(self):
        if self.sprite_type == SpriteType.Simple and self.frame_num is not None:
            raise ValueError("Incorrect sprite configuration")

        return self.frame_num

    def set_source_size(self, source_size: Size):
        self._source_size = source_size

    def get_source_size(self):
        source_size = getattr(self, "_source_size", None)

        if source_size is not None:
            return source_size

    def copy(self):
        data_copy = ImageOptions(
            self.category,
            self.file_name,
            self.name,
            self.sprite_type,
            self.flip,
            self.scale.copy(),
            self.position.copy(),
            self.get_frame_num(),
        )

        image = self.get_image()

        size = self.get_source_size()

        if image is not None:
            data_copy.set_image(image.copy())

        if size is not None:
            data_copy.set_source_size(size)

        return data_copy
