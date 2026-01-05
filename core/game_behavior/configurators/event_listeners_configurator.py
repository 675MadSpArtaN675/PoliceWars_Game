from .. import (
    GameLoopController,
)
from ..event_cores import EventPerformer, KeyEventPerformer
from ..event_cores.data import MouseButton, KeyEvent

import pygame as pg


class EventListenersConfigurator:
    _game_cycle: GameLoopController = None

    event_listener = EventPerformer()
    key_listener = KeyEventPerformer()
    mouse_listener = KeyEventPerformer(True)

    def __init__(self, game_cycle: GameLoopController):
        self._game_cycle = game_cycle

    def ConfigureEventListener(self):
        self._game_cycle.event_listener = self.event_listener

    def ConfigureKeyEventListener(self):
        self._game_cycle.key_listener = self.key_listener

    def ConfigureMouseEventListener(self, **kwargs):
        self._game_cycle.mouse_key_event_listener = self.mouse_listener

        self.mouse_listener.set_event(
            KeyEvent(pg.MOUSEBUTTONDOWN, MouseButton.Left),
            kwargs["object_click_event"],
            kwargs["ui_click_event"],
        )
