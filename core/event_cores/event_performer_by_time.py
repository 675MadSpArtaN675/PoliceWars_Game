from copy import deepcopy

from collections import namedtuple
from typing import Callable

import math as m

EventPerformer_ = Callable[[int], bool]
Event = namedtuple("Event", "time_to_start, function_performer")


class EventPerformerByTime:
    _time: int | float = 0
    _events: dict[str, Event] = None

    def __init__(self):
        self._events = dict()

    def tick(self, delta_time_in_seconds: int | float):
        self._time += delta_time_in_seconds

    def perform_events(self, is_clear_timer: bool = True):
        for name, _ in self._events.items():
            self._perform_event(self._time, name)

        if is_clear_timer:
            self._clear_if_greater_or_equal_max_time()

    def clear_time(self):
        self._time = 0

    def add(
        self,
        name: str,
        time_to_start_in_seconds: int | float,
        performer: EventPerformer_,
    ):
        new_event = Event(time_to_start_in_seconds, performer)

        self._add(name, new_event)

    def _add(self, name: str, new_event: Event):
        if self.is_has_event_with_name(name):
            raise ValueError(f"Event with name {name} already exists")

        self._events[name] = new_event

    def is_has_event_with_name(self, name: str):
        return self._events.get(name) is not None

    def is_empty(self):
        return len(self._events.keys()) <= 0

    def remove_by_name(self, name: str):
        if self.is_has_event_with_name(name):
            del self._events[name]

    def remove_by_performer(self, performer: EventPerformer_):
        self.remove_by_predicate(lambda _, event: event.function_performer == performer)

    def remove_by_time(self, time: int | float, eps: int | float):
        self.remove_by_predicate(
            lambda _, event: m.abs(event.time_to_start - time) <= eps
        )

    def remove_by_predicate(self, predicate: Callable[[Event], bool]):
        if not self.is_empty():
            for name, event in self._events.items():
                if predicate(name, event):
                    del self._events[name]

    def _clear_if_greater_or_equal_max_time(self):
        if not self.is_empty():
            max_time = max(
                self._events.values(), key=lambda x: x.time_to_start
            ).time_to_start

            if self._time >= max_time:
                self.clear_time()

    def _perform_event(self, now_time: int | float, name: str):
        event = self._events.get(name)

        is_called = False
        if event is not None:
            time_to_start = event.time_to_start
            performer = event.function_performer

            if now_time >= time_to_start and performer is not None:
                performer(now_time)
                is_called = True

        return is_called

    def copy(self):
        object_copy = EventPerformerByTime()
        object_copy._events = deepcopy(self._events)

        return object_copy
