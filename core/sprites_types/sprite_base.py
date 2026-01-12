import pygame as pg


class SpriteBase(pg.sprite.Sprite):
    _image: pg.Surface = None
    _rect: pg.Rect = None
    _is_alpha: bool = False

    def __init__(self, width: int, height: int, is_alpha: bool = False):
        super().__init__()

        self._image = pg.Surface((width, height), pg.SRCALPHA)

        if is_alpha:
            self._image = self._image.convert_alpha()
            self._is_alpha = is_alpha

        self._rect = self._image.get_rect()

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def update(self, *args, **kwargs):
        raise NotImplementedError()

    def set_size(self, width: int, height: int):
        self._image = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
        self._rect = self._image.get_rect()

    def get_size(self):
        return self._rect.width, self._rect.height

    def copy(self):
        width = self._rect.width
        height = self._rect.height

        sprite_copy = type(self)(
            width,
            height,
            source_size=self._source_size.copy(),
        )

        sprite_copy._image = self._image.copy()
        sprite_copy._rect = self._image.get_rect()

        return sprite_copy
