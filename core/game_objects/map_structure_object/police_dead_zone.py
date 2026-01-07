from ...sprites_types import SimpleSprite
from ..abstract_objects import CollideableObject, ProcessableObject

from utility_classes.point import Point


class PoliceDeadZone(CollideableObject, ProcessableObject):
    _game_cycle = None

    def __init__(
        self,
        *,
        game_cycle=None,
        sprite: SimpleSprite = None,
        position: Point = Point(),
        depth: int = 0,
    ):
        screen = None
        if game_cycle is not None:
            screen = game_cycle.screen

        super().__init__(screen=screen, sprite=sprite, position=position, depth=depth)

        self._game_cycle = game_cycle

    def end_game(self):
        self._game_cycle.finish_game()

    def process(self, delta_time: int | float, **kwargs):
        enemies = kwargs.get("enemies")

        if enemies is not None:
            for enemy in enemies:
                if self.collision(enemy):
                    self.end_game()
                    break

    def __deepcopy__(self, memo: dict[int, CollideableObject]):
        object_copy = super().__deepcopy__(memo)

        object_copy._game_cycle = self._game_cycle

        return object_copy
