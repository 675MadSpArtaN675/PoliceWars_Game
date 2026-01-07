from .event_performer import EventPerformer
from .data import EventListenerFunction, KeyEvent

import pygame as pg


class KeyEventPerformer(EventPerformer):
    _is_only_mouse_event: bool = False

    def __init__(self, is_mouse_events: bool = False):
        self._is_only_mouse_event = is_mouse_events

    def set_event(
        self,
        event_type_mouse_button: KeyEvent,
        *function_performer: EventListenerFunction,
    ):
        if self._is_only_mouse_event and event_type_mouse_button.event_type not in [
            pg.MOUSEBUTTONDOWN,
            pg.MOUSEBUTTONUP,
        ]:
            raise TypeError("No mouse event!")

        super().set_event(event_type_mouse_button.to_tuple(), *function_performer)

    def perform_event(
        self, event: pg.event.Event, event_type: int = pg.MOUSEBUTTONDOWN
    ):
        if (
            self._is_only_mouse_event
            and event.type == event_type
            and event.button is not None
        ):
            event_performer = self._events.get((event_type, event.button))

            if event_performer is not None and len(event_performer) > 0:
                for performer in event_performer:
                    performer(event)

        elif event.key is not None:
            event_performer = self._events.get(event.key)

            if event_performer is not None and len(event_performer) > 0:
                for performer in event_performer:
                    performer(event)

    def copy(self):
        object_copy = super().copy()

        object_copy._is_only_mouse_event = self._is_only_mouse_event

        return object_copy
