from .. import GameLoopController
from ..texture_loader import TextureLoader

from ..creators import UICreator


class UIConfigurator:
    _game: GameLoopController

    _objects: dict[str, UICreator] = None

    def __init__(self, game_cycle: GameLoopController):
        self._objects = dict()

        self._game = game_cycle

    def configure_window(
        self,
        name: str,
        creator_type: type[UICreator],
        textures_loader: TextureLoader,
        *args,
    ):
        creator = creator_type(name, self._game, textures_loader, *args)

        self._objects[name] = creator

        return self._objects[name]

    def get_ui_window(self, window_name: str):
        ui = self._objects.get(window_name)

        if ui is not None:
            return ui
