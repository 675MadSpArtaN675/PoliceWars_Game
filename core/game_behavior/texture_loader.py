from typing import Generator

from ..sprites_types import load_sprite

import pathlib as pl

import pygame as pg

IMAGE_FORMAT = ".png"


class TextureLoader:
    _textures_dict: dict[str, dict[str, pg.Surface]]

    _texture_folder: pl.Path
    _textures_folders: Generator[pl.Path, None, None]

    def __init__(self, folder_with_textures: str):
        self._texture_folder = pl.Path(folder_with_textures)

        if not self._texture_folder.exists():
            self._texture_folder.mkdir()

        self._textures_folders = self._texture_folder.iterdir()

    def load_textures(self):
        for folder in self._textures_folders:
            if folder.is_dir():
                texture_key = folder.name
                textures = {
                    str(image_file).replace(image_file.suffix, ""): load_sprite(
                        str(image_file)
                    )
                    for image_file in folder.iterdir()
                    if image_file.is_file() and image_file.suffix == IMAGE_FORMAT
                }

                self._textures_dict[texture_key] = textures

    def is_category_exists(self, category: str):
        category = self._textures_dict.get(category)

        return category is not None

    def is_texture_exists(self, category: str, texture: str):
        if self.is_category_exists(category):
            category_textures = self._textures_dict.get(category)
            texture = category_textures.get(texture)

            return texture is not None

        return False

    def get_texture(self, category: str, texture: str):
        return self._textures_dict[category][texture]

    def get_categories(self):
        return self._textures_dict.keys()

    def get_category_textures(self, category: str):
        return self._textures_dict[category].keys()
