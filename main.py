import pygame as pg

from utility_classes.point import Point

from game_objects import ClickableObject, SimpleSprite


pg.init()

screen = pg.display.set_mode((500, 500))
clock = pg.time.Clock()

sp_ss = SimpleSprite(50, 50, pg.Color(0, 0, 255))
sp_clk = SimpleSprite(50, 50, pg.Color(0, 255, 255))

ss = ClickableObject(screen, sp_ss, sp_clk, Point(50, 50))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            print("Presssed Space")
            ss.click()

    screen.fill(pg.Color(255, 0, 0))

    ss.detect()
    ss.render()

    pg.display.flip()
    clock.tick(60)

pg.quit()
