from game_behavior import (
    GameLoopController,
    TextureLoader,
    EventPerformer,
    KeyEventPerformer,
)
from game_behavior.painters import StandartPainter

from game_objects.abstract_objects import GameObject, ClickableObject
from game_objects.sprites_types import SimpleSprite

from utility_classes.point import Point
from utility_classes.size import Size

import pygame as pg


event_listener = EventPerformer()
key_listener = KeyEventPerformer()

game = GameLoopController(Size(1024, 768))
texture_loader = TextureLoader("resources")
game.init_loop()


game.start_cycle()

game.exit()
