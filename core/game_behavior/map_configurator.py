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
    _creators_configurer: ObjectCreatorsConfigurer = None
    _painters: PaintersConfigurer = None
    _object_processor: ObjectProcessorsConfigurer = None
    _game_configurer: GameCycleAdditionsConfigurator = None
    _frame_processor: FrameProcessor = None

    _texture_loader: TextureLoader = None

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

        self._creators_configurer = ObjectCreatorsConfigurer(
            map_object_creator,
            bullet_creator,
            enemy_creator,
            policeman_creator,
        )

    def configure_game(self, window_name: str):
        self._creators_configurer.ui_creator = self._ui_configurer.get_ui_window(
            window_name
        )

        self._painters = PaintersConfigurer(*self._creators_configurer.get_creators())
        self._painters.get_painters()

        self._object_processor = ObjectProcessorsConfigurer(self._creators_configurer)
        self._object_processor.configure()

        self._game_configurer = GameCycleAdditionsConfigurator(
            self._game,
            self._object_processor.click_object_action_performer,
            self._object_processor.ui_clicks_performer,
        )

        self._game_configurer.ConfigureChooser(
            self._creators_configurer.get_objects().policemans
        )
        self._game_configurer.ConfigureEventListeners()

        self._object_processor.configure_unit_processor(
            self._game,
            self._game_configurer.chooser,
        )

        self._creators_configurer.ui_creator.chooser = self._game_configurer.chooser

        self._creators_configurer.create(
            self._object_processor.get_unit_place_function()
        )

        self._frame_processor = FrameProcessor(self._painters, self._object_processor)

    def get_frame_drawer(self):
        if self._frame_processor is not None:
            return self._frame_processor.Draw

        raise ValueError("Map is not configured")
