from .event_performer import EventPerformer, KeyEventPerformer
from utility_classes.size import Size
from .objects_data import GameLoopData
from .unit_processor import UnitProcessor

from typing import Callable

import pygame as pg


FramePerformer = Callable[[pg.Surface, int], None]


class GameLoopController:
    _loop_state: GameLoopData
    _size: Size

    def __init__(self, window_size: Size = Size(), loop_data: GameLoopData = None):
        pg.init()

        if loop_data is None:
            self._loop_state = GameLoopData(window_size)
        else:
            self._loop_state = loop_data

    @property
    def screen(self):
        return self._loop_state.screen

    @property
    def key_listener(self):
        return self._loop_state.key_performer

    @key_listener.setter
    def key_listener(self, listener: KeyEventPerformer):
        if issubclass(type(listener), KeyEventPerformer):
            self._loop_state.key_performer = listener

            return

        raise TypeError("It is not a KeyEventPerformer or it's subclass")

    @property
    def event_listener(self):
        return self._loop_state.event_performer

    @event_listener.setter
    def event_listener(self, listener: EventPerformer):
        if (
            issubclass(type(listener), EventPerformer)
            and type(listener) != KeyEventPerformer
        ):
            listener.set_event(pg.QUIT, self.nice_quit)
            self._loop_state.event_performer = listener

            return

        raise TypeError("It is not a EventPerformer or it's subclass")

    @property
    def mouse_key_event_listener(self):
        return self._loop_state.mouse_key_performer

    @mouse_key_event_listener.setter
    def mouse_key_event_listener(self, listener: EventPerformer):
        if issubclass(type(listener), KeyEventPerformer):
            self._loop_state.mouse_key_performer = listener

            return

        raise TypeError("It is not a EventPerformer or it's subclass")

    @property
    def unit_processor(self):
        return self._unit_processor

    @unit_processor.setter
    def unit_processor(self, processor: UnitProcessor):
        self._unit_processor = processor

    def is_delete_mode_activated(self):
        return self._loop_state.delete_mode

    def delete_mode_activate(self):
        self._loop_state.delete_mode = True

    def delete_mode_deactivate(self):
        self._loop_state.delete_mode = False

    def init_loop(self):
        self._loop_state.init_loop()

    def start_cycle(self, frame_paint_func: FramePerformer = None):
        while self._loop_state.running:
            delta_time = self._loop_state.clock.get_time() / 1000
            self._event_perform_cycle()

            if frame_paint_func is not None:
                frame_paint_func(self._loop_state.screen, delta_time)

            pg.display.flip()
            self._loop_state.clock.tick(60)

    def _event_perform_cycle(self):
        if (
            self._loop_state.event_performer is not None
            or self._loop_state.key_performer is not None
        ):
            for event in pg.event.get():
                if event.type in [pg.KEYUP, pg.KEYDOWN]:
                    self._loop_state.key_performer.perform_event(event)
                elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                    self._loop_state.mouse_key_performer.perform_event(
                        event, event.type
                    )
                else:
                    self._loop_state.event_performer.perform_event(event)

    def nice_quit(self, event=0):
        self._loop_state.running = False

    def exit(self):
        pg.quit()
