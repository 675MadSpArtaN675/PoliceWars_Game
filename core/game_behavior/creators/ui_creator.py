from ...sprites_types import SimpleSprite, SpriteBase
from ..game_loop_controller import GameLoopController
from ..unit_control import UnitChooser

from ..texture_loader import TextureLoader

from ...game_objects.abstract_objects import ClickableObject, GameObject

from utility_classes.point import Point
from .creator import Creator


class UICreator(Creator):
    _window_name: str = None
    _buttons_positions: dict[str, Point] = None

    def __init__(
        self,
        name: str,
        game_cycle: GameLoopController,
        texture_loader: TextureLoader,
        chooser: UnitChooser = None,
        start_objects: list[GameObject] = (),
    ):
        super().__init__(game_cycle, texture_loader, start_objects)
        self._window_name = name
        self._chooser = chooser

        self._buttons_positions = {}

    @property
    def window_name(self):
        return self._window_name

    @property
    def buttons_positions(self):
        return self._buttons_positions

    @buttons_positions.setter
    def buttons_positions(self, positions: dict[str, Point]):
        self._buttons_positions = positions

    def get_buttons_positions_config(self):
        return self.buttons_positions

    def set_buttons_positions_config(self, positions: dict[str, Point]):
        self.buttons_positions = positions

        return self

    @property
    def chooser(self):
        return self._chooser

    @chooser.setter
    def chooser(self, chooser: UnitChooser):
        self._chooser = chooser

    def _create_exit_button(
        self,
        cage_sprite: SpriteBase,
        selection_sprite: SpriteBase,
    ):
        raise NotImplementedError()

    def _create_button(
        self,
        primary_sprite: SimpleSprite,
        secondary_sprite: SimpleSprite,
        position: Point,
        on_clicked_button: callable,
        depth: int,
    ):
        button = ClickableObject(
            screen=self._game_cycle.screen,
            sprite=primary_sprite,
            secondary_sprite=secondary_sprite,
            position=position,
            depth=depth,
        )
        button.on_click_bind(on_clicked_button)

        return button
