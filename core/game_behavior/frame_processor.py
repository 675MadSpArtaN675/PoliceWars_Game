from .configurators import PaintersConfigurer, ObjectProcessorsConfigurer
from ..event_cores import EventPerformerByTime

from ..sprites_types import SimpleSprite
from .bank_system import BankSystem

import pygame as pg


class FrameProcessor:
    _configured_painters: PaintersConfigurer
    _objects_processors: ObjectProcessorsConfigurer
    _timed_events: EventPerformerByTime
    _cycled_timed_events: EventPerformerByTime

    _background: SimpleSprite = None
    _bank_system: BankSystem = None

    def __init__(
        self,
        painters: PaintersConfigurer,
        processors: ObjectProcessorsConfigurer,
        event_performer: EventPerformerByTime,
        cycled_event_performer: EventPerformerByTime,
        background: SimpleSprite,
        bank_system: BankSystem,
    ):
        self._configured_painters = painters
        self._objects_processors = processors
        self._timed_events = event_performer
        self._cycled_timed_events = cycled_event_performer
        self._background = background
        self._bank_system = bank_system

    def Draw(
        self,
        surface: pg.Surface,
        delta_time: int | float,
        is_paused: bool,
        is_ended: bool,
    ):
        self._background.update()

        surface.fill(pg.Color(0, 0, 0))
        surface.blit(
            self._background.image,
            self._background.rect,
        )

        self._timed_events.tick(delta_time)
        self._timed_events.perform_events(False)

        self._cycled_timed_events.tick(delta_time)
        self._cycled_timed_events.perform_events(True)

        self._objects_processors.ui_performer.perform()

        if not is_ended and not is_paused:
            self._object_action_perform(delta_time)

        self._paint_objects(delta_time)

        self._objects_processors.object_deleter.remove_dead_objects()

    def _paint_objects(self, delta_time: int | float):
        self._configured_painters.object_painter.paint_background(delta_time)
        self._configured_painters.object_painter.paint(delta_time)
        self._configured_painters.enemy_painter.paint(delta_time)
        self._configured_painters.bullet_painter.paint(delta_time)
        self._configured_painters.ui_painter.paint(
            delta_time, money_count=self._bank_system.money
        )

    def _object_action_perform(self, delta_time: int | float):
        self._objects_processors.detectable_objects_action_performer.perform()
        self._objects_processors.object_action_performer.perform(delta_time)
        self._objects_processors.enemy_action_performer.perform(delta_time)
        self._objects_processors.policemans_action_performer.perform(delta_time)
        self._objects_processors.bullet_action_performer.perform(delta_time)
