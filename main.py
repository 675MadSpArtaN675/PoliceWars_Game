import pygame as pg

from utility_classes.point import Point

from game_objects.abstract_objects.sprites_types import SimpleSprite
from game_objects.abstract_objects import Bullet

from game_objects.units import MeleeUnit, GunnerUnit
from game_objects import Cell


pg.init()

screen = pg.display.set_mode((500, 500))
clock = pg.time.Clock()


enemy = MeleeUnit(screen, SimpleSprite(50, 50), 100, 100, 15, Point(350, 100))
cell = Cell(
    screen,
    SimpleSprite(50, 50, pg.Color(255, 255, 255)),
    SimpleSprite(50, 50, pg.Color(0, 0, 255)),
)


policeman_buffer = None

delete_mode = False
running = True
while running:
    delta_time = clock.get_time() / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if not delete_mode:
                    print(policeman_buffer)
                    cell.place_unit(policeman_buffer)
                else:
                    cell.delete_unit()

                policeman_buffer = None

            elif event.key == pg.K_f:
                delete_mode = True

            elif event.key == pg.K_0:
                policeman_buffer = GunnerUnit(
                    screen,
                    SimpleSprite(50, 50),
                    SimpleSprite(20, 20),
                    100,
                    500,
                    50,
                    10,
                    Bullet,
                )

            elif event.key == pg.K_1:
                policeman_buffer = GunnerUnit(
                    screen,
                    SimpleSprite(50, 50, pg.Color(50, 50, 0)),
                    SimpleSprite(20, 20),
                    100,
                    500,
                    50,
                    10,
                    Bullet,
                )

    screen.fill(pg.Color(255, 0, 0))

    enemy.render()

    cell.detect()
    cell.render()

    unit = cell.get_unit()

    if unit is not None:
        unit.render()

    pg.display.flip()
    clock.tick(60)

pg.quit()
