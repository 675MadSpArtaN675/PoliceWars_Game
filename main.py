import pygame as pg
import game_objects.gameObject as gameObject

pg.init()

screen = pg.display.set_mode((500, 500))
clock = pg.time.Clock()

sp_ss = gameObject.SimpleSprite(50, 50, pg.Color(0, 255, 0))

running = True
while running:
    for event in pg.event.get():
        print(event, event.type)
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            print("Presssed Space")
            pos = ss.get_position()
            pos.x += 50
            pos.y += 10

            ss.set_position(pos)

    screen.fill(pg.Color(255, 0, 0))
    screen.blit(sp_ss.image, sp_ss.Rect)

    pg.display.flip()
    clock.tick(60)

pg.quit()
