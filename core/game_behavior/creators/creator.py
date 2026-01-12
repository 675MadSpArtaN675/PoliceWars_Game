from .. import GameLoopController

from ...game_objects.abstract_objects import GameObject
from ...sprites_types import SpriteBase

from ...game_behavior import TextureLoader


class Creator:
    category: str = ""

    _game_cycle: GameLoopController = None

    _objects: list[GameObject] = None
    _start_objects: list[GameObject] = None

    _textures: TextureLoader = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        texture_loader: TextureLoader,
        start_objects: list[GameObject] = (),
    ):

        self._game_cycle = game_cycle
        self._start_objects = start_objects
        self._objects = list(start_objects)

        self._textures = texture_loader

    @property
    def textures(self):
        return self._textures

    @textures.setter
    def textures(self, textures: TextureLoader):
        self._textures = textures

    def get_texture_loader(self):
        return self.textures

    def set_texture_loader(self, texture_loader: TextureLoader):
        self.textures = texture_loader

        return self

    def _get_texture(self, name: str):
        return self._textures.get_texture(self.category, name)

    def create(self) -> list[GameObject]:
        self._objects.clear()
        self._objects.extend(list(self._start_objects))

    def get_objects(self) -> list[GameObject]:
        return self._objects
