from .data import EventListenerFunction

from copy import deepcopy

import pygame as pg


class EventPerformer:
    _events: dict[int | tuple, list[EventListenerFunction]] = dict()

    def __init__(self):
        self._events = dict()

    def perform_event(self, event: pg.event.Event):
        event_performer = self._events.get(event.type)

        if event_performer is not None and len(event_performer) > 0:
            for performer in event_performer:
                performer(event)

    def set_event(self, event_type: int, *function_performer: EventListenerFunction):
        if self._events.get(event_type) is None:
            self._events[event_type] = []

        self._events[event_type].extend(function_performer)

    def remove_event(self, event_type: int):
        if self._events.get(event_type) is not None:
            self._events[event_type].clear()

    def copy(self):
        performer_copy = EventPerformer()
        performer_copy._events = deepcopy(self._events)

        return performer_copy
