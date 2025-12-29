from typing import Callable
from enum import IntEnum, auto
import pygame as pg

EventListenerFunction = Callable[[pg.event.Event], None]


class MouseButton(IntEnum):
    Left: int = 1
    Middle: int = auto()
    Right: int = auto()


class EventPerformer:
    _events: dict[int | tuple, EventListenerFunction] = dict()

    def __init__(self):
        self._events = dict()

    def perform_event(self, event: pg.event.Event):
        event_performer = self._events.get(event.type)

        if event_performer is not None:
            event_performer(event)

    def set_event(self, event_type: int, function_performer: EventListenerFunction):
        self._events[event_type] = function_performer

    def remove_event(self, event_type: int):
        if self._events.get(event_type) is not None:
            self._events.pop(event_type)


class KeyEventPerformer(EventPerformer):
    _is_only_mouse_event: bool = False

    def __init__(self, is_mouse_events: bool = False):
        self._is_only_mouse_event = is_mouse_events

    def perform_event(
        self, event: pg.event.Event, event_type: int = pg.MOUSEBUTTONDOWN
    ):
        try:
            if (
                self._is_only_mouse_event
                and event.type == event_type
                and event.button is not None
            ):
                event_performer = self._events.get((event_type, event.button))

                if event_performer is not None:
                    event_performer(event)

            elif event.key is not None:
                event_performer = self._events.get(event.key)

                if event_performer is not None:
                    event_performer(event)

        except AttributeError as ex:
            print(ex)
