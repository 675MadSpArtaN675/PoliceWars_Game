from game_behavior import GameLoopController

from game_objects.units import MeleeUnit
from .creator import Creator


class EnemyCreator(Creator):
    _objects: list[MeleeUnit] = None

    def __init__(
        self, game_cycle: GameLoopController, start_units: list[MeleeUnit] = ()
    ):
        self._game_cycle = game_cycle
        self._objects = list(start_units)

    def create(self):
        for ready_unit in self._objects:
            ready_unit.is_can_move = True
            ready_unit.is_can_attack = True

        return self._objects

    def get_objects(self):
        return self._objects
