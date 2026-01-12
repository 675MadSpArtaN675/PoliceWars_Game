from ..creators import (
    PolicemansCreator,
    MapObjectsCreator,
    BulletCreator,
    EnemyCreator,
    UICreator,
)

from .data import ObjectsByLevels


class ObjectCreatorsConfigurer:
    __slots__ = [
        "policemans_creator",
        "bullets_creator",
        "enemy_creator",
        "map_creator",
        "_ui_creator",
        "_unit_processor",
    ]

    policemans_creator: PolicemansCreator
    bullets_creator: BulletCreator
    enemy_creator: EnemyCreator
    map_creator: MapObjectsCreator

    _ui_creator: UICreator

    def __init__(
        self,
        map_creator: MapObjectsCreator,
        bullets_creator: BulletCreator,
        enemies_creator: EnemyCreator,
        policemans_creator: PolicemansCreator,
        ui_creator: UICreator = None,
    ):
        self.map_creator = map_creator
        self.bullets_creator = bullets_creator
        self.enemy_creator = enemies_creator
        self.policemans_creator = policemans_creator
        self._ui_creator = ui_creator

    @property
    def ui_creator(self):
        return self._ui_creator

    @ui_creator.setter
    def ui_creator(self, creator: UICreator):
        self._ui_creator = creator

    def create(self, to_place_unit_on_grid_function: callable):
        self.map_creator.func_placer = to_place_unit_on_grid_function

        self.policemans_creator.create()
        self.map_creator.create()
        self.bullets_creator.create()
        self.enemy_creator.create()
        self._ui_creator.create()

    def get_creators(self):
        return (
            self.map_creator,
            self.enemy_creator,
            self.bullets_creator,
            self.ui_creator,
        )

    def get_objects(self):
        return ObjectsByLevels(
            *self.policemans_creator.get_objects(),
            *self.map_creator.get_objects(),
            self.bullets_creator.get_objects(),
            self.enemy_creator.get_objects(),
            self._ui_creator.get_objects(),
        )
