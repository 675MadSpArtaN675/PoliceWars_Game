from .creators import (
    Creator,
    PolicemansCreator,
    MapObjectsCreator,
    BulletCreator,
    EnemyCreator,
)

from .game_loop_controller import GameLoopController
from .action_performer import ActionPerformer
from .object_deleter import ObjectDeleter
from .painters import StandartPainter, ObjectPainter
from .unit_control import UnitChooser
from .unit_processor import UnitProcessor

from .configurators.event_listeners_configurator import EventListenersConfigurator


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

    _object_deleter: ObjectDeleter = None

    _ui_painter = StandartPainter()
    _object_painter = ObjectPainter()
    _enemy_painter = StandartPainter()
    _bullet_painter = StandartPainter()

    _ui_performer = ActionPerformer()
    _ui_clicks_performer = ActionPerformer()

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

        self._object_deleter = ObjectDeleter()

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
        self._object_painter.add(*self._map_creator.get_objects())
        self._enemy_painter.add(self._enemy_creator.get_objects())
        self._bullet_painter.add(self._bullets_creator.get_objects())
        self._ui_painter.add(self._ui_creator.get_objects())

    def ConfigureActionPerformers(self):
        policemans, working_units = self._policemans_creator.get_objects()
        map_objects, clickable_map_objects = self._map_creator.get_objects()
        bullet_objects = self._bullets_creator.get_objects()
        enemies_objects = self._enemy_creator.get_objects()
        ui_objects = self._ui_creator.get_objects()

        self._object_deleter.add(
            policemans,
            map_objects,
            clickable_map_objects,
            working_units,
            bullet_objects,
            enemies_objects,
            ui_objects,
        )

        self._ui_performer.add(ui_objects)
        self._ui_clicks_performer.add(ui_objects)

        self._object_action_performer.add(map_objects)
        self._detectable_objects_action_performer.add(clickable_map_objects)
        self._bullet_action_performer.add(bullet_objects)
        self._click_object_action_performer.add(clickable_map_objects)
        self._policemans_action_performer.add(working_units)
        self._enemy_action_performer.add(enemies_objects)

        self._object_action_performer.performers = partial(
            self._map_creator.process_object, enemies=enemies_objects
        )
        self._detectable_objects_action_performer.performers = (
            lambda game_object: game_object.detect()
        )

        self._click_object_action_performer.performers = (
            lambda game_object, _: game_object.click()
        )

        self._ui_performer.performers = lambda game_object: game_object.detect()
        self._ui_clicks_performer.performers = (
            lambda game_object, _: game_object.click()
        )

    def ConfigureUnitProcessor(self, unit_processor: UnitProcessor):
        if unit_processor is not None:
            self._unit_processor = unit_processor

            _, working_units = self._policemans_creator.get_objects()
            enemies_objects = self._enemy_creator.get_objects()
            bullets = self._bullets_creator.get_objects()

            self._bullet_action_performer.performers = partial(
                self._unit_processor.process,
                objects_to_collide_list=[working_units, enemies_objects],
            )
            self._enemy_action_performer.performers = partial(
                self._unit_processor.process,
                objects_to_collide_list=[working_units, bullets],
            )

            self._policemans_action_performer.performers = partial(
                self._unit_processor.process,
                objects_to_collide_list=[enemies_objects, bullets],
            )

    def ConfigureChooser(self):
        if self._chooser is None:
            self._chooser = UnitChooser(self._policemans_creator.get_objects()[0])

    def ConfigureEventListeners(self):
        self._listeners = EventListenersConfigurator(self._game_cycle)

        self._listeners.ConfigureEventListener()
        self._listeners.ConfigureKeyEventListener()
        self._listeners.ConfigureMouseEventListener(
            object_click_event=self._click_object_action_performer.perform,
            ui_click_event=self._ui_clicks_performer.perform,
        )

    def Draw(
        self,
        surface: pg.Surface,
        delta_time: int | float,
        is_paused: bool,
        is_ended: bool,
    ):
        surface.fill(pg.Color(0, 255, 0))

        self._ui_performer.perform()

        if not is_ended and not is_paused:
            self._object_action_perform(delta_time)

        self._paint_objects()

        self._object_deleter.remove_dead_objects()

    def _paint_objects(self):
        self._object_painter.paint_background()
        self._object_painter.paint()
        self._enemy_painter.paint()
        self._bullet_painter.paint()
        self._ui_painter.paint()

    def _object_action_perform(self, delta_time: int | float):
        self._detectable_objects_action_performer.perform()
        self._object_action_performer.perform(delta_time)
        self._enemy_action_performer.perform(delta_time)
        self._policemans_action_performer.perform(delta_time)
        self._bullet_action_performer.perform(delta_time)
