from .. import GameLoopController

from ..unit_control import UnitChooser

from ..creators import Creator


class UIConfigurator:
    _chooser: UnitChooser
    _game: GameLoopController

    _objects: dict[str, Creator] = None

    def __init__(self, game_cycle: GameLoopController, chooser: UnitChooser):
        self._objects = dict()

        self._game = game_cycle
        self._chooser = chooser

    def configure_window(self, name: str, creator_type: type, *args):
        self._objects[name] = creator_type(self._game, self._chooser, *args)

        return self._objects

    def get_ui_window(self, window_name: str):
        ui = self._objects.get(window_name)

        if ui is not None:
            return ui
