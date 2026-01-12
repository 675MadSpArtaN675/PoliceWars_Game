from ..sprites_types import SimpleSprite

from .sprite_parser import ImageParser, ImageOptions

from utility_classes import Size

import pathlib as pl
import random as r

import pygame as pg

IMAGE_FORMAT = ".png"


class TextureLoader:
    _image_parser: ImageParser = None
    _sprite_size: Size = None
    _textures_dict: dict[str, dict[str, pg.Surface]] = None

    _texture_folder: pl.Path = None

    def __init__(
        self,
        folder_with_textures: str,
        time_between_frames: int = 5,
        texture_standart_size: Size = Size(64, 64),
    ):
        self._textures_dict = {}
        self._texture_folder = pl.Path(folder_with_textures)

        self._sprite_size = texture_standart_size
        self._image_parser = ImageParser(texture_standart_size, time_between_frames)

        if not self._texture_folder.exists():
            raise ImportError("Error to open resource directory")

    def load_textures(self, configs: list[ImageOptions]):
        textures_folders = self._texture_folder.iterdir()
        name_parser = lambda image_file: str(image_file.name).replace(
            image_file.suffix, ""
        )

        for folder in textures_folders:
            if folder.is_dir():
                texture_key = folder.name
                textures = {
                    name_parser(image_file): self.load_sprite(
                        texture_key, name_parser(image_file), image_file, configs
                    )
                    for image_file in folder.iterdir()
                    if image_file.is_file() and image_file.suffix == IMAGE_FORMAT
                }

                self._textures_dict[texture_key] = textures

        print(f"Loaded textures: {self._textures_dict}...")

    def load_sprite(
        self,
        category: str,
        file_name: str,
        image_path: str,
        configs: list[ImageOptions],
    ):
        image = pg.image.load(image_path)

        result = []
        for config in configs:
            if config.category == category and config.file_name == file_name:
                config.set_image(image)
                result.append(config)

        return self._image_parser.parse_images(result)

    def is_textures_loaded(self):
        return len(self._textures_dict.items()) > 0

    def is_category_exists(self, category: str):
        category_ = self._textures_dict.get(category)

        return category_ is not None

    def is_texture_exists(self, category: str, texture: str):
        if self.is_category_exists(category):
            category_textures = self._textures_dict.get(category)
            texture_ = category_textures.get(texture)

            return texture_ is not None

        return False

    def is_state_exists(self, category: str, texture: str, state: str):
        if self.is_texture_exists(category, texture):
            category_ = self._textures_dict.get(category)
            texture_ = category_.get(texture)
            state_ = texture_.get(state, None)

            return state_ is not None

        return False

    def get_texture(self, category: str, texture: str, state: str = ""):
        if not bool(state) and self.is_texture_exists(category, texture):
            category_ = self._textures_dict.get(category)
            texture_ = category_.get(texture)

            return texture_.copy()

        if self.is_state_exists(category, texture, state):
            category_ = self._textures_dict.get(category)
            texture_ = category_.get(texture)
            state_ = texture_.get(state)

            return state_.copy()

        color_byte_1 = r.randint(0, 255)
        color_byte_2 = r.randint(0, 255)
        color_byte_3 = r.randint(0, 255)

        return SimpleSprite(
            *self._sprite_size.to_tuple(),
            pg.Color(color_byte_1, color_byte_2, color_byte_3),
        )

    def get_categories(self):
        return self._textures_dict.keys()

    def get_category_textures(self, category: str):
        if self.is_category_exists(category):
            return self._textures_dict.get(category).keys()

        return {}
