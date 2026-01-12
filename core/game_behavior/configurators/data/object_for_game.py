from ....game_objects.abstract_objects import GameObject, ClickableObject
from ....game_objects.units import MeleeUnit, Bullet

from dataclasses import dataclass


@dataclass
class ObjectsByLevels:
    __slots__ = [
        "policemans",
        "policemans_working_units",
        "map_objects",
        "clickable_map_objects",
        "bullet_objects",
        "enemies_objects",
        "ui_objects",
    ]

    policemans: list[MeleeUnit]
    policemans_working_units: list[MeleeUnit]
    map_objects: list[GameObject]
    clickable_map_objects: list[ClickableObject]
    bullet_objects: list[Bullet]
    enemies_objects: list[MeleeUnit]
    ui_objects: list[ClickableObject]

    def to_tuple(self):
        return (
            self.policemans,
            self.policemans_working_units,
            self.map_objects,
            self.clickable_map_objects,
            self.bullet_objects,
            self.enemies_objects,
            self.ui_objects,
        )

    def __getitem__(self, index: int | slice):
        start_index, stop_index, step = index.start, index.stop, index.step

        if start_index is None:
            start_index = 0

        if stop_index is None:
            stop_index = len(self.to_tuple())

        if step is None:
            step = 1

        creators_list = self.to_tuple()

        return creators_list[start_index:stop_index:step]
