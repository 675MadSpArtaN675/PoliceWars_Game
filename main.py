from game_behavior import GameLoopController, UnitProcessor

from game_objects.sprites_types import SimpleSprite
from game_objects.units import MeleeUnit, GunnerUnit, Bullet

from game_behavior.objects_data import UnitFraction
from game_behavior.configurators import (
    ObjectManager,
    UIConfigurator,
)
from game_behavior.creators import (
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
        10,
        6,
        UnitFraction.Police,
    ),
]

enemy_creator = EnemyCreator(game)
policeman_creator = PolicemansCreator(game, units_to_choose)
bullet_creator = BulletCreator(game)
map_object_creator = MapObjectsCreator(game, Size(5, 10))


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
        object_configurer.chooser,
        policeman_creator.get_objects()[1],
        bullet_creator.get_objects(),
    )
)
object_configurer.ConfigureEventListeners()

object_configurer.CreateObjects()

game.start_cycle(object_configurer.Draw)

game.exit()
