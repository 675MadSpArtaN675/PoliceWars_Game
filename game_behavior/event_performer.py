from typing import Callable

import pygame as pg

EventListenerFunction = Callable[[pg.event.Event], None]


class EventPerformer:
    _events: dict[int, EventListenerFunction] = dict()

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
    def perform_event(self, event: pg.event.Event):
        try:
            if event.key is not None:
                event_performer = self._events.get(event.key)

                if event_performer is not None:
                    event_performer(event)

        except AttributeError as ex:
            print(ex)
