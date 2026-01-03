from game_behavior import GameLoopController

from game_objects.units import MeleeUnit
from .creator import Creator


class PolicemansCreator(Creator):
    _objects: list[MeleeUnit] = None
    _working_objects: list[MeleeUnit] = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        start_units: list[MeleeUnit] = (),
        start_working_units: list[MeleeUnit] = (),
    ):
        self._game_cycle = game_cycle
        self._objects = list(start_units)
        self._working_objects = list(start_working_units)

    def create(self):
        for ready_unit in self._objects:
            ready_unit.is_can_move = False

        for ready_unit in self._working_objects:
            ready_unit.is_can_move = False

        return self._objects, self._working_objects

    def get_objects(self):
        return self._objects, self._working_objects
