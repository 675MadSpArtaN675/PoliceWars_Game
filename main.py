from core.game_behavior import (
    GameLoopController,
    UnitProcessor,
    ObjectManager,
    TextureLoader,
)

from core.sprites_types import SimpleSprite

from core.game_objects.units import MeleeUnit, GunnerUnit, Bullet
from core.game_objects.map_structure_object.spawners_data import UnitList, UnitToSpawn

from core.objects_data import UnitFraction

from core.game_behavior.configurators import UIConfigurator
from core.game_behavior.creators import (
    EnemyCreator,
    BulletCreator,
    PolicemansCreator,
    MapObjectsCreator,
    BattleUICreator,
)


from utility_classes.size import Size


import pygame as pg


game = GameLoopController(Size(1024, 768))
game.init_loop()
texture_loader = TextureLoader("resourses")


enemy_units = UnitList(
    [
        UnitToSpawn(
            MeleeUnit(
                game.screen,
                SimpleSprite(50, 50, pg.Color(255, 255, 255)),
                100,
                10,
                -10,
                UnitFraction.Terrorists,
            ),
            50,
        ),
        UnitToSpawn(
            MeleeUnit(
                game.screen,
                SimpleSprite(50, 50, pg.Color(255, 255, 125)),
                100,
                15,
                -5,
                UnitFraction.Terrorists,
            ),
            10,
        ),
        UnitToSpawn(
            MeleeUnit(
                game.screen,
                SimpleSprite(50, 50, pg.Color(255, 255, 125)),
                125,
                25,
                -2,
                UnitFraction.Terrorists,
            ),
            10,
        ),
    ]
)

units_to_choose = [
    MeleeUnit(
        game.screen,
        SimpleSprite(50, 50, pg.Color(0, 50, 0)),
        100,
        20,
        10,
        UnitFraction.Police,
    ),
    GunnerUnit(
        game.screen,
        SimpleSprite(50, 50, pg.Color(0, 200, 0)),
        SimpleSprite(25, 25, pg.Color(255, 255, 0)),
        100,
        0,
        10,
        100,
        Bullet,
        11,
        3,
        UnitFraction.Police,
        show_detector=True,
    ),
]

enemy_creator = EnemyCreator(game)
policeman_creator = PolicemansCreator(game, units_to_choose)
bullet_creator = BulletCreator(game)
map_object_creator = MapObjectsCreator(game, Size(5, 10), enemy_units)


object_configurer = ObjectManager(
    game, map_object_creator, bullet_creator, enemy_creator, policeman_creator
)

object_configurer.ConfigureChooser()

ui_configurer = UIConfigurator(game, object_configurer.chooser)
ui_configurer.configure_window("battle_ui", BattleUICreator, 15)

object_configurer.ui_creator = ui_configurer.get_ui_window("battle_ui")
object_configurer.ConfigurePainters()

object_configurer.ConfigureActionPerformers()
object_configurer.ConfigureUnitProcessor(
    UnitProcessor(
        game,
        object_configurer.chooser,
        policeman_creator.get_objects()[1],
        bullet_creator.get_objects(),
    )
)
object_configurer.ConfigureEventListeners()

object_configurer.CreateObjects()

game.start_cycle(object_configurer.Draw)

game.exit()
