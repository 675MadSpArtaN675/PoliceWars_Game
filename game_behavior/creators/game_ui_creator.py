from game_behavior import GameLoopController

from game_objects.abstract_objects import ClickableObject, GameObject
from game_behavior.unit_control import UnitChooser
from game_objects.sprites_types import SimpleSprite

from utility_classes.point import Point

from .creator import Creator

import pygame as pg


class BattleUICreator(Creator):
    _chooser: UnitChooser = None

    _dx_between_buttons: int = 15

    def __init__(
        self,
        game_cycle: GameLoopController,
        chooser: UnitChooser,
        distance_between_unit_button: int,
        start_objects: list[GameObject] = (),
    ):
        super().__init__(game_cycle, start_objects)

        self._chooser = chooser
        self._dx_between_buttons = distance_between_unit_button

    def create(self) -> list[GameObject]:
        exit_button = self._create_exit_button()
        self._create_unit_buttons(self._dx_between_buttons)

        self._objects.append(exit_button)

        return self._objects

    def get_objects(self) -> list[GameObject]:
        return self._objects

    def _create_unit_buttons(self, _dx_between_buttons: int):
        dx = 0
        dx_between_buttons = _dx_between_buttons
        pos = Point(50, 15)
        for func in self._chooser.get_setter_functions():
            unit_button = self._create_button(
                SimpleSprite(50, 50, pg.Color(0, 0, 50 + dx)),
                SimpleSprite(50, 50),
                pos.copy(),
                func,
            )

            if dx == 0:
                dx += 50 + dx_between_buttons

            pos += Point(dx, 0)

            self._objects.append(unit_button)

    def _create_exit_button(self):
        return self._create_button(
            SimpleSprite(50, 50, pg.Color(0, 0, 50)),
            SimpleSprite(50, 50),
            Point(950, 15),
            self._game_cycle.nice_quit,
        )

    def _create_button(
        self,
        primary_sprite: SimpleSprite,
        secondary_sprite: SimpleSprite,
        position: Point,
        on_clicked_button,
    ):
        button = ClickableObject(
            self._game_cycle.screen,
            primary_sprite,
            secondary_sprite,
            position,
        )
        button.on_click_bind(on_clicked_button)

        return button
