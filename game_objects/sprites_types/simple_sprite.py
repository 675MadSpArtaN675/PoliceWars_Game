import pygame as pg


class SimpleSprite(pg.sprite.Sprite):
    __resourse_image: pg.Surface
    _color: pg.Color

    _image: pg.Surface
    _rect: pg.Rect

    def __init__(
        self,
        width: int,
        height: int,
        color: pg.Color = pg.Color(0, 0, 0),
        image: pg.Surface = None,
    ):
        super().__init__()

        self._image = pg.Surface((width, height))
        self._rect = self._image.get_rect()

        self.__resourse_image = image
        self._color = color

    @property
    def Image(self):
        return self._image

    @property
    def Rect(self):
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
