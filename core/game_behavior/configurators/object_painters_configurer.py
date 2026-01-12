from ...game_objects.abstract_objects import GameObject

from ..creators import (
    Creator,
    MapObjectsCreator,
    BulletCreator,
    EnemyCreator,
)

from ..painters import ObjectPainter, StandartPainter

from .data_enum import ObjectPaintLevel


class PaintersConfigurer:
    __slots__ = ["ui_painter", "object_painter", "enemy_painter", "bullet_painter"]

    object_painter: ObjectPainter
    enemy_painter: StandartPainter
    bullet_painter: StandartPainter
    ui_painter: StandartPainter

    def __init__(
        self,
        map_creator: MapObjectsCreator,
        enemy_creator: EnemyCreator,
        bullet_creator: BulletCreator,
        ui_creator: Creator,
    ):
        self.object_painter = ObjectPainter()
        self.enemy_painter = StandartPainter()
        self.bullet_painter = StandartPainter()
        self.ui_painter = StandartPainter()

        self.object_painter.add(*map_creator.get_objects())
        self.enemy_painter.add(enemy_creator.get_objects())
        self.bullet_painter.add(bullet_creator.get_objects())
        self.ui_painter.add(ui_creator.get_objects())

    def add(self, level: ObjectPaintLevel, objects: list[GameObject]):
        match (level):
            case ObjectPaintLevel.ui:
                self.ui_painter.add(objects)
            case ObjectPaintLevel.bullet:
                self.bullet_painter.add(objects)
            case ObjectPaintLevel.enemy:
                self.enemy_painter.add(objects)
            case ObjectPaintLevel.objects:
                self.object_painter.add(objects)

            case _:
                raise NotImplementedError("No level found")

    def get_painters(self):
        return (
            self.object_painter,
            self.enemy_painter,
            self.bullet_painter,
            self.ui_painter,
        )
