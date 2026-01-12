from .configurators import PaintersConfigurer, ObjectProcessorsConfigurer

import pygame as pg


class FrameProcessor:
    _configured_painters: PaintersConfigurer
    _objects_processors: ObjectProcessorsConfigurer

    def __init__(
        self, painters: PaintersConfigurer, processors: ObjectProcessorsConfigurer
    ):
        self._configured_painters = painters
        self._objects_processors = processors

    def Draw(
        self,
        surface: pg.Surface,
        delta_time: int | float,
        is_paused: bool,
        is_ended: bool,
    ):
        surface.fill(pg.Color(0, 255, 0))

        self._objects_processors.ui_performer.perform()

        if not is_ended and not is_paused:
            self._object_action_perform(delta_time)

        self._paint_objects()

        self._objects_processors.object_deleter.remove_dead_objects()

    def _paint_objects(self):
        self._configured_painters.object_painter.paint_background()
        self._configured_painters.object_painter.paint()
        self._configured_painters.enemy_painter.paint()
        self._configured_painters.bullet_painter.paint()
        self._configured_painters.ui_painter.paint()

    def _object_action_perform(self, delta_time: int | float):
        self._objects_processors.detectable_objects_action_performer.perform()
        self._objects_processors.object_action_performer.perform(delta_time)
        self._objects_processors.enemy_action_performer.perform(delta_time)
        self._objects_processors.policemans_action_performer.perform(delta_time)
        self._objects_processors.bullet_action_performer.perform(delta_time)
