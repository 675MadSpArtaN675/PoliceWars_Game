import pygame as pg

from utility_classes.point import Point

from game_objects.abstract_objects import ClickableObject
from game_objects.sprites_types import SimpleSprite
from game_objects.map_structure_object import UnitLine, Cell, UnitGrid

pg.init()

screen = pg.display.set_mode((800, 700))
clock = pg.time.Clock()

grid = UnitGrid(screen, 10, 10, Point(10, 10), -5)
grid.cell_sprite = SimpleSprite(50, 50)
grid.selected_cell_sprite = SimpleSprite(50, 50, pg.Color(0, 0, 255))

grid.build()

delete_mode = False
running = True
while running:
    delta_time = clock.get_time() / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(pg.Color(255, 0, 0))

    grid.render()

    pg.display.flip()
    clock.tick(60)

pg.quit()
