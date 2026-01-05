from .. import GameLoopController

from ...game_objects.abstract_objects import GameObject


class Creator:
    _game_cycle: GameLoopController = None
    _objects: list[GameObject] = None
    _start_objects: list[GameObject] = None

    def __init__(
        self, game_cycle: GameLoopController, start_objects: list[GameObject] = ()
    ):
        self._game_cycle = game_cycle
        self._start_objects = start_objects
        self._objects = list(start_objects)

    def create(self) -> list[GameObject]:
        self._objects.clear()
        self._objects.extend(list(self._start_objects))

    def get_objects(self) -> list[GameObject]:
        return self._objects
