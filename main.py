from game_behavior import (
    GameLoopController,
    TextureLoader,
    EventPerformer,
    KeyEventPerformer,
    MouseButton,
)

from game_behavior import ActionPerformer
from game_behavior.painters import StandartPainter, ObjectPainter

from game_objects import Detector
from game_objects.abstract_objects import ClickableObject, GameObject
from game_behavior.unit_control import UnitChooser, UnitCreator
from game_objects.sprites_types import SimpleSprite
from game_objects.map_structure_object import UnitGrid
from game_objects.units import MeleeUnit, GunnerUnit, Bullet
from game_behavior.objects_data import UnitType, UnitFraction

from utility_classes.point import Point
from utility_classes.size import Size

from functools import partial

import pygame as pg

ui = []
policemans = []
bullets = []
map_objects = []
background_objects = []

ui_painter = StandartPainter()
object_painter = ObjectPainter()
enemy_painter = StandartPainter()
bullet_painter = StandartPainter()

button_action_performer = ActionPerformer()
object_action_performer = ActionPerformer()
click_object_action_performer = ActionPerformer()
enemy_action_performer = ActionPerformer()
policemans_action_performer = ActionPerformer()
bullet_action_performer = ActionPerformer()

start_game = False


def Draw(surface: pg.Surface, delta_time):
    surface.fill(pg.Color(0, 255, 0))

    if start_game:
        button_action_performer.perform()
        object_action_performer.perform()
        enemy_action_performer.perform(delta_time)
        policemans_action_performer.perform(delta_time)
        bullet_action_performer.perform(delta_time)

        button_action_performer.remove_dead_objects()
        enemy_action_performer.remove_dead_objects()
        policemans_action_performer.remove_dead_objects()
        object_action_performer.remove_dead_objects()
        click_object_action_performer.remove_dead_objects()
        bullet_action_performer.remove_dead_objects()

    object_painter.paint_background()
    object_painter.paint()
    enemy_painter.paint()
    bullet_painter.paint()
    # detector.render()
    ui_painter.paint()

    object_painter.remove_dead_objects()
    enemy_painter.remove_dead_objects()
    bullet_painter.remove_dead_objects()
    ui_painter.remove_dead_objects()


def UnitProcessor(
    unit: MeleeUnit | GunnerUnit,
    delta_time: int | float,
    objects_to_collide_list: list[MeleeUnit | GunnerUnit] = (),
):
    if unit.health <= 0:
        unit.destroy()

    collide = False
    for object_to_collide in objects_to_collide_list:
        if (
            not object_to_collide.is_dead()
            and object_to_collide.team != unit.team
            and unit.collision(object_to_collide)
        ):
            unit.attack(object_to_collide, 1.0)

            if object_to_collide.health < 1:
                object_to_collide.destroy()

            collide = True
            break

    if not collide and unit.is_can_move:
        unit.move(delta_time)

    if issubclass(type(unit), Bullet) and collide:
        unit.destroy()
        return

    if issubclass(type(unit), GunnerUnit):
        if (
            unit.is_can_attack
            and not collide
            and unit.is_detect(objects_to_collide_list)
        ):
            shoot_bullet = unit.shoot(1.0, delta_time)

            if shoot_bullet is not None:
                bullets.append(shoot_bullet)


def PolicePlace():
    unit = chooser.extract_unit()
    policemans.append(unit)

    return unit


event_listener = EventPerformer()
key_listener = KeyEventPerformer()
mouse_listener = KeyEventPerformer(True)

game = GameLoopController(Size(1024, 768))
game.event_listener = event_listener
game.key_listener = key_listener
game.mouse_key_event_listener = mouse_listener

texture_loader = TextureLoader("resources")
texture_loader.load_textures()


def start(event):
    global start_game
    start_game = True


key_listener.set_event(pg.K_SPACE, start)

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
    MeleeUnit(
        game.screen,
        SimpleSprite(50, 50, pg.Color(0, 125, 0)),
        100,
        35,
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

units_to_choose[2].IsNeedToShowDetector = True


for ready_unit in units_to_choose:
    ready_unit.is_can_move = False

chooser = UnitChooser(units_to_choose)

enemies = [
    MeleeUnit(
        game.screen,
        SimpleSprite(50, 50),
        100,
        10,
        -10,
        UnitFraction.Terrorists,
        position=Point(500, 275),
    )
]

detector = Detector(game.screen, Size(50, 50), 5, position=Point(100, 275))
detector.refresh()


exit_button = ClickableObject(
    game.screen,
    SimpleSprite(50, 50, pg.Color(0, 0, 50)),
    SimpleSprite(50, 50),
    Point(950, 15),
)
exit_button.on_click_bind(game.nice_quit)

ui.append(exit_button)

dx = 0
dx_between_buttons = 15
pos = Point(50, 15)
for func in chooser.get_setter_functions():
    button = ClickableObject(
        game.screen,
        SimpleSprite(50, 50, pg.Color(0, 0, 50 + dx)),
        SimpleSprite(50, 50),
        pos.copy(),
    )
    button.on_click_bind(func)

    ui.append(button)

    if dx == 0:
        dx += 50 + dx_between_buttons
    pos += Point(dx, 0)


unit_grid = UnitGrid(game.screen, 5, 10, Point(100, 225), -100)

unit_grid.cell_sprite = SimpleSprite(50, 50, pg.Color(255, 0, 0))
unit_grid.selected_cell_sprite = SimpleSprite(50, 50, pg.Color(0, 0, 255))
unit_grid.on_click_bind(PolicePlace)
unit_grid.build()

map_objects.append(unit_grid)

ui_painter.objects = ui
object_painter.objects = map_objects
enemy_painter.objects = enemies
bullet_painter.objects = bullets

object_action_performer.objects = map_objects
button_action_performer.objects = ui
bullet_action_performer.objects = bullets
click_object_action_performer.objects = ui + map_objects
policemans_action_performer.objects = policemans
enemy_action_performer.objects = enemies

object_action_performer.func_performer = lambda game_object: game_object.detect()
button_action_performer.func_performer = lambda game_object: game_object.detect()
bullet_action_performer.func_performer = partial(
    UnitProcessor, objects_to_collide_list=policemans + enemies
)
click_object_action_performer.func_performer = lambda game_object: game_object.click()
enemy_action_performer.func_performer = partial(
    UnitProcessor, objects_to_collide_list=policemans
)

policemans_action_performer.func_performer = partial(
    UnitProcessor, objects_to_collide_list=enemies
)


mouse_listener.set_event(
    (pg.MOUSEBUTTONDOWN, MouseButton.Left),
    lambda x: click_object_action_performer.perform(),
)

game.start_cycle(Draw)

game.exit()
