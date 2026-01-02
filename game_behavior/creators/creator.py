from typing import Callable

from game_behavior import GameLoopController

from game_objects.abstract_objects import ClickableObject, GameObject
from game_behavior.unit_control import UnitChooser
from game_objects.sprites_types import SimpleSprite
from game_objects.map_structure_object import UnitGrid
from game_objects.units import MeleeUnit, Bullet

from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


class Creator:
    _game_cycle: GameLoopController = None
    _objects: list[GameObject] = None

    def __init__(
        self, game_cycle: GameLoopController, start_objects: list[GameObject] = ()
    ):
        self._game_cycle = game_cycle
        self._objects = list(start_objects)

    def create(self) -> list[GameObject]:
        raise NotImplemented()

    def get_objects(self) -> list[GameObject]:
        raise NotImplemented()
