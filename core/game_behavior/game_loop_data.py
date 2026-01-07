from ..event_cores import EventPerformer, KeyEventPerformer

from utility_classes.size import Size


import pygame as pg


class GameLoopData:
    _size: Size

    screen: pg.Surface = None
    clock: pg.time.Clock = None

    running: bool = True
    paused: bool = False
    ended: bool = False
    delete_mode: bool = False

    key_performer: KeyEventPerformer = None
    mouse_key_performer: KeyEventPerformer = None
    event_performer: EventPerformer = None

    def __init__(self, window_size: Size):
        self._size = window_size

    def init_loop(self):
        if pg.get_init():
            self.screen = pg.display.set_mode((self._size.width, self._size.height))
            self.clock = pg.time.Clock()
