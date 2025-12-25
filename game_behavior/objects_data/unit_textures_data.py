from utility_classes.point import Point
from utility_classes.size import Size

from dataclasses import dataclass

import pygame as pg


@dataclass
class TextureData:
    size: Size

    def to_tuple(self):
        raise NotImplementedError()


class ColoredTextureData(TextureData):
    color: pg.Color = pg.Color(0, 0, 0)


class ImageTextureData(TextureData):
    image_path: str
