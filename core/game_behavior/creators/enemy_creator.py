from ...game_behavior import GameLoopController

from ...game_objects.units import MeleeUnit
from .creator import Creator


class EnemyCreator(Creator):
    _objects: list[MeleeUnit] = None

    def __init__(
        self, game_cycle: GameLoopController, start_units: list[MeleeUnit] = ()
    ):
        super().__init__(game_cycle, start_units)

    def create(self):
        super().create()

        for ready_unit in self._objects:
            ready_unit.is_can_move = True
            ready_unit.is_can_attack = True

        return self._objects
