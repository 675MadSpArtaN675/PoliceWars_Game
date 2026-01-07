from utility_classes.size import Size

import pygame as pg

import pathlib as pl


class SimpleSprite(pg.sprite.Sprite):
    __image_path: str = None
    __resourse_image: str = None
    _color: pg.Color = None

    _image: pg.Surface = None
    _rect: pg.Rect = None

    def __init__(
        self,
        width: int,
        height: int,
        color: pg.Color = pg.Color(0, 0, 0),
        image_path: str = None,
    ):
        super().__init__()

        self.__image_path = image_path
        self._image = pg.Surface((width, height))
        self._rect = self._image.get_rect()

        if image_path is not None and image_path.strip() != "":
            self.__resourse_image = pg.image.load(image_path)

        self._color = color

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def update(self, *args, **kwargs):
        if self.__resourse_image is not None:
            image = pg.transform.scale(
                self.__resourse_image, (self._rect.width, self._rect.height)
            )
            self._image.blit(image, (0, 0))

        elif self._color is not None:
            self._image.fill(self._color)

    def set_size(self, width: int, height: int):
        self._image = pg.Surface((width, height))
        self._rect = self._image.get_rect()

    def copy(self):
        width = self._rect.width
        height = self._rect.height

        sprite_copy = SimpleSprite(width, height)

        sprite_copy._image = self._image.copy()
        sprite_copy._rect = self._image.get_rect()
        sprite_copy._color = pg.Color(self._color.r, self._color.g, self._color.b)

        return sprite_copy


def load_sprite(path_to_image: str, size: Size):
    path_image = pl.Path(path_to_image).absolute()
    image = pg.image.load(path_image)
    transformed_image = pg.transform.scale(image, size.to_tuple())

    return SimpleSprite(*size, image_path=transformed_image)
