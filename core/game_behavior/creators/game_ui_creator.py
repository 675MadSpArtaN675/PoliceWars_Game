from ...sprites_types import SpriteBase

from .. import GameLoopController

from ...game_objects.abstract_objects import GameObject

from ..bank_system import BankSystem
from ...game_objects.ui import MoneyDisplay

from ..unit_control import UnitChooser
from ..texture_loader import TextureLoader

from utility_classes import Point, Size

from .ui_creator import UICreator

import pygame as pg


class BattleUICreator(UICreator):
    category: str = "ui"

    bank_performer: BankSystem = None
    _dx_between_buttons: int = 25

    def __init__(
        self,
        name: str,
        game_cycle: GameLoopController,
        texture_loader: TextureLoader,
        distance_between_unit_button: int,
        chooser: UnitChooser = None,
        start_objects: list[GameObject] = (),
    ):
        super().__init__(name, game_cycle, texture_loader, chooser, start_objects)

        self._dx_between_buttons = distance_between_unit_button

    def create(self) -> list[GameObject]:
        super().create()

        unit_buttons = self._create_unit_buttons(
            self._get_texture("unit_button", "base"),
            self._get_texture("unit_button", "base"),
        )
        money_displayer_ = self._create_money_displayer(
            20, "C:\\windows\\Fonts\\georgia.ttf"
        )

        exit_button = self._create_exit_button(
            self._get_texture("exit_button", "base"),
            self._get_texture("exit_button", "base"),
        )
        pause_button = self._create_pause_game_button(
            self._get_texture("pause_button", "base"),
            self._get_texture("pause_button", "base"),
        )
        delete_mode_button = self._create_delete_mode_game_button(
            self._get_texture("delete_mode_button", "base"),
            self._get_texture("delete_mode_button", "base"),
        )

        self._objects.extend(unit_buttons)
        self._objects.append(money_displayer_)
        self._objects.append(pause_button)
        self._objects.append(exit_button)
        self._objects.append(delete_mode_button)

        return self._objects

    def _create_unit_buttons(
        self,
        cage_sprite: SpriteBase,
        selection_sprite: SpriteBase,
    ):
        result = []

        dx = 0
        pos = self._buttons_positions.get("unit_buttons", Point())
        for _, func in self._chooser.get_units_with_their_setter_functions():
            unit_button = self._create_button(
                cage_sprite, selection_sprite, pos.copy(), func, 100
            )

            if dx == 0:
                dx += 50 + self._dx_between_buttons

            pos += Point(dx, 0)

            result.append(unit_button)

        return result

    def _create_money_displayer(self, font_size: int, font_name: str):
        money_displayer = MoneyDisplay(
            self._game_cycle.screen,
            Size(120, font_size * 2),
            font_size,
            font_name,
            pg.Color(0, 0, 0),
            "Ваш счёт: {}$",
            self._buttons_positions.get("money_display", Point()),
            100,
        )

        return money_displayer

    def _create_exit_button(
        self,
        primary_sprite: SpriteBase,
        selection_sprite: SpriteBase,
    ):
        return self._create_button(
            primary_sprite,
            selection_sprite,
            self._buttons_positions.get("exit_button", Point()),
            self._game_cycle.nice_quit,
            100,
        )

    def _create_pause_game_button(
        self, primary_sprite: SpriteBase, selection_sprite: SpriteBase
    ):
        return self._create_button(
            primary_sprite,
            selection_sprite,
            self._buttons_positions.get("pause_button", Point()),
            self._game_cycle.pause_toggle,
            100,
        )

    def _create_delete_mode_game_button(
        self, primary_sprite: SpriteBase, selection_sprite: SpriteBase
    ):
        return self._create_button(
            primary_sprite,
            selection_sprite,
            self._buttons_positions.get("delete_mode_button", Point()),
            self._game_cycle.delete_mode_toggle,
            100,
        )
