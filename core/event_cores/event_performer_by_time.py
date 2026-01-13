from copy import deepcopy

from collections import namedtuple
from typing import Callable

import math as m

EventPerformer_ = Callable[[int], bool]


class EventTime:
    _time_to_start: int | float = 0
    _function_performer: EventPerformer_ = None

    is_performed_in_iteration: bool = False

    def __init__(self, time_to_start: float | int, function_performer: EventPerformer_):
        self._time_to_start = time_to_start
        self._function_performer = function_performer

    def __deepcopy__(self, memo):
        object_copy = EventTime(self._time_to_start, self._function_performer)

        memo[id(self)] = self
        memo[id(object_copy)] = object_copy

        return object_copy

    @property
    def time_to_start(self):
        return self._time_to_start

    @property
    def function_performer(self):
        return self._function_performer

    def set_performed_status(self, flag: bool):
        self.is_performed_in_iteration = flag

    def get_performed_status(self):
        return self.is_performed_in_iteration


class EventPerformerByTime:
    _time: int | float = 0
    _events: dict[str, EventTime] = None

    def __init__(self):
        self._events = dict()

    def tick(self, delta_time_in_seconds: int | float):
        self._time += delta_time_in_seconds

    def perform_events(self, is_clear_timer: bool = True):
        for name, _ in self._events.items():
            self._perform_event(self._time, name, not is_clear_timer)

        if is_clear_timer:
            self._clear_if_greater_or_equal_max_time()

        self.clear_performed_status()

    def clear(self):
        self._events.clear()

    def clear_time(self):
        self._time = 0

    def clear_performed_status(self):
        for event in self._events.values():
            event.is_performed_in_iteration = False

    def add(
        self,
        name: str,
        time_to_start_in_seconds: int | float,
        performer: EventPerformer_,
    ):
        new_event = EventTime(time_to_start_in_seconds, performer)

        self._add(name, new_event)

    def _add(self, name: str, new_event: EventTime):
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

    def remove_by_predicate(self, predicate: Callable[[EventTime], bool]):
        if not self.is_empty():
            for name, event in self._events.items():
                if predicate(name, event):
                    del self._events[name]

    def _clear_if_greater_or_equal_max_time(self):
        if not self.is_empty():
            max_time = max(
                self._events.values(), key=lambda x: x.time_to_start
            ).time_to_start

            if self._time - max_time > 0.0:
                self.clear_time()

    def _perform_event(self, now_time: int | float, name: str, is_need_clear: bool):
        event = self._events.get(name)

        is_called = False
        if event is not None:
            time_to_start = event.time_to_start
            performer = event.function_performer

            delta_now_max = now_time - time_to_start

            if (
                delta_now_max > 0.0
                and (delta_now_max < 0.02 or is_need_clear)
                and performer is not None
            ):
                if not event.is_performed_in_iteration:
                    performer(now_time)
                    event.is_performed_in_iteration = True

                is_called = True

        return is_called

    def copy(self):
        object_copy = EventPerformerByTime()
        object_copy._events = deepcopy(self._events)

        return object_copy
