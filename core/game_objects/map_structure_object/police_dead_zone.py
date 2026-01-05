from ...sprites_types import SimpleSprite
from ..abstract_objects import CollideableObject, ProcessableObject

from utility_classes.point import Point


class PoliceDeadZone(CollideableObject, ProcessableObject):
    _game_cycle = None

    def __init__(
        self,
        game_cycle,
        sprite: SimpleSprite,
        /,
        position: Point = Point(),
        depth: int = 0,
    ):
        super().__init__(game_cycle.screen, sprite, position=position, depth=depth)

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
