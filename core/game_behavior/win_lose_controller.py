from .game_loop_controller import GameLoopController

from ..game_objects.units import MeleeUnit


class WinLoseController:
    _game_cycle: GameLoopController = None

    enemies_objects: list[MeleeUnit] = None

    def __init__(self, game: GameLoopController, enemies_objects: list[MeleeUnit]):
        self._game_cycle = game
        self.enemies_objects = enemies_objects

    def finish_game_when_time_no_remains(self, delta_time: int | float):
        if len(self.enemies_objects) <= 0:
            self._game_cycle.finish_game()
