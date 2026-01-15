from .win_lose_controller import WinLoseController

from .game_loop_controller import GameLoopController
from .frame_processor import FrameProcessor
from .texture_loader import TextureLoader

from .configurators import (
    GameCycleAdditionsConfigurator,
    ObjectCreatorsConfigurer,
    PaintersConfigurer,
    ObjectProcessorsConfigurer,
    UIConfigurator,
)

from ..event_cores import EventPerformerByTime
from ..game_objects.units import MeleeUnit

from .configurators import UIConfigurator
from .creators import (
    EnemyCreator,
    BulletCreator,
    PolicemansCreator,
    MapObjectsCreator,
)


from utility_classes import Size, Point


class LevelConfigurer:
    _game: GameLoopController = None
    _plant_grid_size: Size = None

    _ui_configurer: UIConfigurator = None
    _painters: PaintersConfigurer = None
    _object_processor: ObjectProcessorsConfigurer = None
    _game_configurer: GameCycleAdditionsConfigurator = None
    _frame_processor: FrameProcessor = None

    _texture_loader: TextureLoader = None

    creators_configurer: ObjectCreatorsConfigurer = None

    def __init__(
        self,
        game_cycle: GameLoopController,
        cell_size: Size,
        ui_configurator: UIConfigurator,
    ):
        self._game = game_cycle
        self._plant_grid_size = cell_size

        self._ui_configurer = ui_configurator

    @property
    def textures_loader(self):
        return self._texture_loader

    @textures_loader.setter
    def textures_loader(self, loader: TextureLoader):
        self._texture_loader = loader

    def configure_creators(
        self,
        friendly_units_to_choose: list[MeleeUnit],
        enemy_patterns: list[MeleeUnit],
        grid_position: Point,
        distance_between_grid_and_spawners: int = 1,
    ):
        enemy_creator = EnemyCreator(self._game)
        policeman_creator = PolicemansCreator(
            self._game, start_units=friendly_units_to_choose
        )
        bullet_creator = BulletCreator(self._game)
        map_object_creator = MapObjectsCreator(
            self._game, self._plant_grid_size, enemy_patterns
        )
        map_object_creator.textures = self._texture_loader
        map_object_creator.unit_grid_position = grid_position
        map_object_creator.distance_in_cells_count = distance_between_grid_and_spawners

        self.creators_configurer = ObjectCreatorsConfigurer(
            map_object_creator,
            bullet_creator,
            enemy_creator,
            policeman_creator,
        )

    def configure_game(self, window_name: str, time_to_win: int, start_money: int):
        self.creators_configurer.ui_creator = self._ui_configurer.get_ui_window(
            window_name
        )

        background = self._texture_loader.get_sprite(
            "map_object_texture", "background", "base"
        )
        size = self._game.get_window_size()
        size.width += 76

        background.set_size_with_subimage(*size.to_tuple())

        win_lose = WinLoseController(
            self._game, self.creators_configurer.enemy_creator.get_objects()
        )

        self._painters = PaintersConfigurer(*self.creators_configurer.get_creators())
        self._painters.get_painters()

        self._object_processor = ObjectProcessorsConfigurer(
            self.creators_configurer, start_money
        )
        self._object_processor.configure()

        self._game_configurer = GameCycleAdditionsConfigurator(
            self._game,
            self._object_processor.click_object_action_performer,
            self._object_processor.ui_clicks_performer,
        )

        self._game_configurer.ConfigureChooser(
            self.creators_configurer.get_objects().policemans
        )
        self._game_configurer.ConfigureEventListeners()

        self._object_processor.configure_unit_processor(
            self._game, self._game_configurer.chooser
        )

        self.creators_configurer.ui_creator.chooser = self._game_configurer.chooser

        self.creators_configurer.create(
            self._object_processor.get_unit_place_function()
        )

        self._time_event_controller = EventPerformerByTime()
        self._time_event_controller.add(
            "win", time_to_win, win_lose.finish_game_when_time_no_remains
        )

        self._cycled_time_event_controller = EventPerformerByTime()
        self._cycled_time_event_controller.add(
            "money_give",
            5,
            lambda _: self._object_processor.get_bank_system().add_money(50),
        )

        self._frame_processor = FrameProcessor(
            self._painters,
            self._object_processor,
            self._time_event_controller,
            self._cycled_time_event_controller,
            background,
            self._object_processor.get_bank_system(),
        )

    def get_frame_drawer(self):
        if self._frame_processor is not None:
            return self._frame_processor.Draw

        raise ValueError("Map is not configured")
