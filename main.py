from core.game_behavior import (
    GameLoopController,
    UnitProcessor,
    ObjectManager,
    TextureLoader,
)

from core.sprites_types import SimpleSprite

from core.game_objects.units import MeleeUnit, GunnerUnit, Bullet, BulletData
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


from utility_classes import Size, Point

import pygame as pg


game = GameLoopController(Size(1024, 768))
game.init_loop()
texture_loader = TextureLoader("resourses")


enemy_units = UnitList(
    [
        UnitToSpawn(
            MeleeUnit(
                screen=game.screen,
                sprite=SimpleSprite(50, 50, pg.Color(255, 255, 255)),
                health=100,
                damage=10,
                speed=-10,
                team=UnitFraction.Terrorists,
            ),
            50,
        ),
        UnitToSpawn(
            MeleeUnit(
                screen=game.screen,
                sprite=SimpleSprite(50, 50, pg.Color(255, 255, 125)),
                health=100,
                damage=15,
                speed=-5,
                team=UnitFraction.Terrorists,
            ),
            10,
        ),
        UnitToSpawn(
            MeleeUnit(
                screen=game.screen,
                sprite=SimpleSprite(50, 50, pg.Color(255, 255, 125)),
                health=125,
                damage=25,
                speed=-4,
                team=UnitFraction.Terrorists,
            ),
            10,
        ),
    ]
)


units_to_choose = [
    MeleeUnit(
        screen=game.screen,
        sprite=SimpleSprite(50, 50, pg.Color(0, 50, 0)),
        health=100,
        damage=20,
        speed=10,
        team=UnitFraction.Police,
    ),
    GunnerUnit(
        screen=game.screen,
        sprite=SimpleSprite(50, 50, pg.Color(0, 200, 0)),
        health=100,
        melee_damage=5,
        bullet=Bullet(
            screen=game.screen,
            sprite=SimpleSprite(15, 15),
            bullet_data=BulletData(100, 30, 100, Point(50, 15)),
            team=UnitFraction.Police,
        ),
        speed=0,
        shoot_distance=10,
        shoot_interval=3,
        team=UnitFraction.Police,
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
