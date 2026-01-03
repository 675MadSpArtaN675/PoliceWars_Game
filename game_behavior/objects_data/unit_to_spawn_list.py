from .unit_to_spawn import UnitToSpawn
from game_objects.units import MeleeUnit


class UnitList:
    _units: list[UnitToSpawn]

    def __init__(self, units: list[UnitToSpawn]):
        self._units = units

    def __getitem__(self, key: int):
        if key < len(self._units) and key >= 0:
            return self._units[key].unit.copy()

        raise IndexError("List index out of range")

    def __len__(self):
        return len(self._units)

    @property
    def weights(self):
        return tuple(map(lambda x: x.ratio, self._units))

    @property
    def unit_objects(self):
        return tuple(map(lambda x: x.unit, self._units))

    @property
    def units_full_data(self):
        return tuple(self._units)

    def weight_sum(self):
        return sum(self.weights)

    def append(self, unit: MeleeUnit, ratio: int | float):
        if unit is not None:
            unit = UnitToSpawn(unit, ratio)

            self._units.append(unit)
