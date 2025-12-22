import pygame as pg

from utility_classes.point import Point

from game_objects.abstract_objects.sprites_types import SimpleSprite
from game_objects import Bullet, BanditUnit


pg.init()

screen = pg.display.set_mode((500, 500))
clock = pg.time.Clock()

sp_ss = SimpleSprite(50, 50, pg.Color(0, 0, 255))
sp_clk = SimpleSprite(50, 50, pg.Color(0, 255, 255))

bul = Bullet(screen, sp_ss, 100, 100, 100, Point(0, 100))
enemy = BanditUnit(screen, sp_clk, -1, 50, -15, Point(350, 100))

start_damage = False
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            print("Presssed Space")
            start_damage = True

    screen.fill(pg.Color(255, 0, 0))

    enemy_health = enemy.health
    enemy.move(clock.get_time() / 1000)

    if bul is not None and not bul.collision(enemy):
        bul.move(clock.get_time() / 1000)

    if bul is not None and start_damage and bul.collision(enemy):
        bul.attack(enemy, 5)
        bul.destroy()
        bul = None

    enemy.render()

    if bul is not None:
        bul.render()

    pg.display.flip()
    clock.tick(60)

pg.quit()
