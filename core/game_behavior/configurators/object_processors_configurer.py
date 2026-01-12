from ..game_loop_controller import GameLoopController
from ..unit_control import UnitChooser

from ...game_objects.abstract_objects import (
    GameObject,
    ClickableObject,
    ProcessableObject,
)
from ...game_objects.units import MeleeUnit, Bullet

from ..action_performer import ActionPerformer
from ..object_deleter import ObjectDeleter
from ..unit_processor import UnitProcessor

from .object_creators_configurer import ObjectCreatorsConfigurer

from functools import partial


class ObjectProcessorsConfigurer:
    ui_performer: ActionPerformer = None
    ui_clicks_performer: ActionPerformer = None
    detectable_objects_action_performer: ActionPerformer = None
    object_action_performer: ActionPerformer = None
    click_object_action_performer: ActionPerformer = None
    enemy_action_performer: ActionPerformer = None
    policemans_action_performer: ActionPerformer = None
    bullet_action_performer: ActionPerformer = None

    object_deleter: ObjectDeleter = None

    _unit_processor: UnitProcessor = None

    _creators: ObjectCreatorsConfigurer = None

    def __init__(self, creators: ObjectCreatorsConfigurer):
        self.ui_performer = ActionPerformer()
        self.ui_clicks_performer = ActionPerformer()
        self.detectable_objects_action_performer = ActionPerformer()
        self.object_action_performer = ActionPerformer()
        self.click_object_action_performer = ActionPerformer()
        self.enemy_action_performer = ActionPerformer()
        self.policemans_action_performer = ActionPerformer()
        self.bullet_action_performer = ActionPerformer()

        self.object_deleter = ObjectDeleter()

        self._creators = creators

    @property
    def creators(self):
        return self._creators

    @creators.setter
    def creators(self, creators: ObjectCreatorsConfigurer):
        self._creators = creators

    def configure(self):
        _, working_units = self._creators.policemans_creator.get_objects()
        map_objects, clickable_map_objects = self._creators.map_creator.get_objects()
        bullet_objects = self._creators.bullets_creator.get_objects()
        enemies_objects = self._creators.enemy_creator.get_objects()
        ui_objects = self._creators.ui_creator.get_objects()

        self._add_objects_to_performers(
            working_units,
            map_objects,
            clickable_map_objects,
            bullet_objects,
            enemies_objects,
            ui_objects,
        )

        self._set_functions_to_performers(enemies_objects)

        objects_lists = self._creators.get_objects()
        self.object_deleter.add(
            objects_lists.bullet_objects,
            objects_lists.clickable_map_objects,
            objects_lists.policemans_working_units,
            objects_lists.map_objects,
            objects_lists.ui_objects,
        )

    def configure_unit_processor(self, game: GameLoopController, chooser: UnitChooser):
        bullets = self._creators.bullets_creator.get_objects()
        _, working_units = self._creators.policemans_creator.get_objects()
        enemies_objects = self._creators.enemy_creator.get_objects()

        self._unit_processor = UnitProcessor(game, chooser, working_units, bullets)

        self._configure_units(working_units, enemies_objects, bullets)

    def get_unit_process_function(self):
        return self._unit_processor.process

    def get_unit_place_function(self):
        return self._unit_processor.police_place

    def _add_objects_to_performers(
        self,
        working_units: list[MeleeUnit],
        map_objects: list[ProcessableObject],
        clickable_map_objects: list[ClickableObject],
        bullet_objects: list[Bullet],
        enemies_objects: list[MeleeUnit],
        ui_objects: list[GameObject],
    ):
        self.ui_performer.add(ui_objects)
        self.ui_clicks_performer.add(ui_objects)

        self.object_action_performer.add(map_objects)
        self.detectable_objects_action_performer.add(clickable_map_objects)
        self.click_object_action_performer.add(clickable_map_objects)

        self.policemans_action_performer.add(working_units)
        self.enemy_action_performer.add(enemies_objects)
        self.bullet_action_performer.add(bullet_objects)

    def _configure_units(self, working_units, enemies_objects, bullet_objects):
        self.policemans_action_performer.performers = partial(
            self._unit_processor.process,
            objects_to_collide_list=[bullet_objects, enemies_objects],
        )
        self.enemy_action_performer.performers = partial(
            self._unit_processor.process,
            objects_to_collide_list=[working_units, bullet_objects],
        )
        self.bullet_action_performer.performers = partial(
            self._unit_processor.process,
            objects_to_collide_list=[working_units, enemies_objects],
        )

    def _set_functions_to_performers(self, enemies_objects: list[MeleeUnit]):
        self.object_action_performer.performers = partial(
            self._creators.map_creator.process_object, enemies=enemies_objects
        )
        self.detectable_objects_action_performer.performers = (
            lambda game_object: game_object.detect()
        )

        self.click_object_action_performer.performers = (
            lambda game_object, _: game_object.click()
        )

        self.ui_performer.performers = lambda game_object: game_object.detect()
        self.ui_clicks_performer.performers = lambda game_object, _: game_object.click()
