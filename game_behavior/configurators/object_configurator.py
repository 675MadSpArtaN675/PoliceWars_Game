from ..creators import (
    Creator,
    PolicemansCreator,
    MapObjectsCreator,
    BulletCreator,
    EnemyCreator,
)

from game_behavior import ActionPerformer
from game_behavior.painters import StandartPainter, ObjectPainter
from game_behavior.unit_control import UnitChooser


from .event_listeners_configurator import EventListenersConfigurator
from game_behavior.unit_processor import UnitProcessor
from game_behavior import GameLoopController

from functools import partial

import pygame as pg


class ObjectManager:
    _chooser: UnitChooser = None
    _listeners: EventListenersConfigurator = None

    _game_cycle: GameLoopController = None

    _policemans_creator: PolicemansCreator = None
    _map_creator: MapObjectsCreator = None
    _bullets_creator: BulletCreator = None
    _enemy_creator: EnemyCreator = None
    _ui_creator: Creator = None

    _ui_painter = StandartPainter()
    _object_painter = ObjectPainter()
    _enemy_painter = StandartPainter()
    _bullet_painter = StandartPainter()

    _detectable_objects_action_performer = ActionPerformer()
    _object_action_performer = ActionPerformer()
    _click_object_action_performer = ActionPerformer()
    _enemy_action_performer = ActionPerformer()
    _policemans_action_performer = ActionPerformer()
    _bullet_action_performer = ActionPerformer()

    _unit_processor: UnitProcessor = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        map_creator: MapObjectsCreator,
        bullets_creator: BulletCreator,
        enemies_creator: EnemyCreator,
        policemans_creator: PolicemansCreator,
    ):
        self._game_cycle = game_cycle
        self._map_creator = map_creator
        self._bullets_creator = bullets_creator
        self._enemy_creator = enemies_creator
        self._policemans_creator = policemans_creator

    @property
    def chooser(self):
        return self._chooser

    @property
    def ui_creator(self):
        return self._ui_creator

    @ui_creator.setter
    def ui_creator(self, creator: Creator):
        self._ui_creator = creator

    def CreateObjects(self):
        self._map_creator.func_placer = self._unit_processor.police_place

        self._policemans_creator.create()
        self._map_creator.create()
        self._bullets_creator.create()
        self._enemy_creator.create()
        self._ui_creator.create()

    def ConfigurePainters(self):
        self._object_painter.objects = self._map_creator.get_objects()
        self._enemy_painter.objects = self._enemy_creator.get_objects()
        self._bullet_painter.objects = self._bullets_creator.get_objects()
        self._ui_painter.objects = self._ui_creator.get_objects()

    def ConfigureActionPerformers(self):
        policemans = self._policemans_creator.get_objects()
        map_objects = self._map_creator.get_objects()
        bullet_objects = self._bullets_creator.get_objects()
        enemies_objects = self._enemy_creator.get_objects()
        ui_objects = self._ui_creator.get_objects()

        self._object_action_performer.add(map_objects)
        self._detectable_objects_action_performer.add(ui_objects)
        self._bullet_action_performer.add(bullet_objects)
        self._click_object_action_performer.add(ui_objects, map_objects)
        self._policemans_action_performer.add(policemans)
        self._enemy_action_performer.add(enemies_objects)

        self._object_action_performer.func_performer = (
            lambda game_object: game_object.detect()
        )
        self._detectable_objects_action_performer.func_performer = (
            lambda game_object: game_object.detect()
        )
        self._click_object_action_performer.func_performer = (
            lambda game_object, _: game_object.click()
        )

    def ConfigureUnitProcessor(self, unit_processor: UnitProcessor):
        if unit_processor is not None:
            self._unit_processor = unit_processor

            policemans = self._policemans_creator.get_objects()
            enemies_objects = self._enemy_creator.get_objects()

            self._bullet_action_performer.func_performer = partial(
                self._unit_processor.process,
                objects_to_collide_list=[policemans, enemies_objects],
            )
            self._enemy_action_performer.func_performer = partial(
                self._unit_processor.process, objects_to_collide_list=[policemans]
            )

            self._policemans_action_performer.func_performer = partial(
                self._unit_processor.process, objects_to_collide_list=[enemies_objects]
            )

    def ConfigureChooser(self):
        if self._chooser is None:
            self._chooser = UnitChooser(self._policemans_creator.get_objects())

    def ConfigureEventListeners(self):
        self._listeners = EventListenersConfigurator(self._game_cycle)

        self._listeners.ConfigureEventListener()
        self._listeners.ConfigureKeyEventListener()
        self._listeners.ConfigureMouseEventListener(
            object_click_event=self._click_object_action_performer.perform
        )

    def Draw(self, surface: pg.Surface, delta_time):
        surface.fill(pg.Color(0, 255, 0))

        self._object_action_perform(delta_time)
        self._paint_objects()

        self._remove_dead_objects_from_performers()
        self._remove_dead_objects_from_painters()

    def _remove_dead_objects_from_painters(self):
        self._object_painter.remove_dead_objects()
        self._enemy_painter.remove_dead_objects()
        self._bullet_painter.remove_dead_objects()
        self._ui_painter.remove_dead_objects()

    def _paint_objects(self):
        self._object_painter.paint_background()
        self._object_painter.paint()
        self._enemy_painter.paint()
        self._bullet_painter.paint()
        self._ui_painter.paint()

    def _remove_dead_objects_from_performers(self):
        self._detectable_objects_action_performer.remove_dead_objects()
        self._enemy_action_performer.remove_dead_objects()
        self._policemans_action_performer.remove_dead_objects()
        self._object_action_performer.remove_dead_objects()
        self._click_object_action_performer.remove_dead_objects()
        self._bullet_action_performer.remove_dead_objects()

    def _object_action_perform(self, delta_time: int | float):
        self._detectable_objects_action_performer.perform()
        self._object_action_performer.perform()
        self._enemy_action_performer.perform(delta_time)
        self._policemans_action_performer.perform(delta_time)
        self._bullet_action_performer.perform(delta_time)
