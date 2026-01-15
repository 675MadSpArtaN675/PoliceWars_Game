from core.game_behavior import (
    GameLoopController,
    TextureLoader,
    LevelConfigurer,
)
from core.game_behavior.creators import BattleUICreator

from core.sprites_types import SimpleSprite
from core.sprites_types.data import ImageOptions, SpriteType, FlipSide

from core.game_objects.units import MeleeUnit, GunnerUnit, Bullet, BulletData
from core.game_objects.map_structure_object.spawners_data import UnitList, UnitToSpawn

from core.objects_data import UnitFraction

from core.game_behavior.configurators import UIConfigurator

from utility_classes import Size, Point

win_size = Size(1024, 768)
game = GameLoopController(win_size)
game.init_loop()


configs = [
    ImageOptions(
        "map_object_texture",
        "background",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1.0, 1.0),
        Point(0, 0),
    ),
    ImageOptions(
        "policeman",
        "policeman",
        "stay",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1.5, 1.5),
        Point(0, 0),
    ),
    ImageOptions(
        "policeman",
        "policeman",
        "shoot",
        SpriteType.Animated,
        FlipSide.NoFlip,
        Size(1.5, 1.5),
        Point(0, 0),
        1,
    ),
    ImageOptions(
        "policeman",
        "policeman",
        "shoot",
        SpriteType.Animated,
        FlipSide.NoFlip,
        Size(1.5, 1.5),
        Point(64, 0),
        2,
    ),
    ImageOptions(
        "policeman",
        "policeman",
        "dead",
        SpriteType.Animated,
        FlipSide.NoFlip,
        Size(1.5, 1.5),
        Point(0, 64),
        1,
    ),
    ImageOptions(
        "policeman",
        "middle_policeman",
        "stay",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1.5, 1.5),
        Point(0, 0),
    ),
    ImageOptions(
        "policeman",
        "middle_policeman",
        "dead",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1.5, 1.5),
        Point(0, 64),
    ),
    ImageOptions(
        "map_object_texture",
        "unit_cell",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "map_object_texture",
        "selected_unit_cell",
        "select",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "enemies",
        "standart_niggers",
        "standart_nigger",
        SpriteType.Simple,
        FlipSide.Horizontal,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "enemies",
        "standart_niggers",
        "middle_nigger",
        SpriteType.Simple,
        FlipSide.Horizontal,
        Size(1, 1),
        Point(0, -64),
    ),
    ImageOptions(
        "enemies",
        "standart_niggers",
        "strong_nigger",
        SpriteType.Simple,
        FlipSide.Horizontal,
        Size(1, 1),
        Point(0, -128),
    ),
    ImageOptions(
        "projectile",
        "standart_bullet",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "ui",
        "exit_button",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "ui",
        "delete_mode_button",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "ui",
        "pause_button",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
    ImageOptions(
        "ui",
        "unit_button",
        "base",
        SpriteType.Simple,
        FlipSide.NoFlip,
        Size(1, 1),
        Point(0, 0),
    ),
]

texture_loader = TextureLoader("resourses/textures")
texture_loader.load_textures(configs)

enemy_units = UnitList(
    [
        UnitToSpawn(
            MeleeUnit(
                screen=game.screen,
                sprite=texture_loader.get_sprite(
                    "enemies", "standart_niggers", "standart_nigger"
                ),
                health=50,
                damage=5,
                speed=-25,
                team=UnitFraction.Terrorists,
                off_detector=True,
            ),
            50,
        ),
        UnitToSpawn(
            MeleeUnit(
                screen=game.screen,
                sprite=texture_loader.get_sprite(
                    "enemies", "standart_niggers", "middle_nigger"
                ),
                health=125,
                damage=15,
                speed=-10,
                team=UnitFraction.Terrorists,
                off_detector=True,
            ),
            25,
        ),
        UnitToSpawn(
            MeleeUnit(
                screen=game.screen,
                sprite=texture_loader.get_sprite(
                    "enemies", "standart_niggers", "strong_nigger"
                ),
                health=200,
                damage=25,
                speed=-5,
                team=UnitFraction.Terrorists,
                off_detector=True,
            ),
            2,
        ),
    ]
)

bullet_texture = texture_loader.get_sprite(
    "projectile", "standart_bullet", "base", Size(10, 10)
)

standart_bullet = Bullet(
    screen=game.screen,
    sprite=bullet_texture,
    bullet_data=BulletData(20, 125, 20, Point(50, 15)),
    team=UnitFraction.Police,
)

units_to_choose = [
    GunnerUnit(
        screen=game.screen,
        sprite=texture_loader.get_sprite("policeman", "policeman", "stay"),
        health=100,
        melee_damage=10,
        bullet=standart_bullet,
        speed=0,
        shoot_distance=7,
        shoot_interval=5,
        team=UnitFraction.Police,
        price=100,
    ),
    GunnerUnit(
        screen=game.screen,
        sprite=texture_loader.get_sprite("policeman", "middle_policeman", "stay"),
        health=100,
        melee_damage=10,
        bullet=standart_bullet,
        speed=0,
        shoot_distance=10,
        shoot_interval=4,
        team=UnitFraction.Police,
        price=150,
    ),
]

ui_config = {
    "unit_buttons": Point(25, 25),
    "money_display": Point(25, 100),
    "exit_button": Point(win_size.width - 100, 25),
    "pause_button": Point(win_size.width - 170, 25),
    "delete_mode_button": Point(win_size.width - 100, win_size.height - 84),
}

ui_configurer = UIConfigurator(game)
ui_configurer.configure_window(
    "battle_ui", BattleUICreator, texture_loader, 25
).set_buttons_positions_config(ui_config)


level = LevelConfigurer(game, Size(5, 10), ui_configurer)
level.textures_loader = texture_loader
level.configure_creators(units_to_choose, enemy_units, Point(12, 152), 5)
level.configure_game("battle_ui", 180, 0)

game.start_cycle(level.get_frame_drawer())

game.exit()
