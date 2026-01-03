from game_objects.units import MeleeUnit


class UnitToSpawn:
    _unit: MeleeUnit
    _spawn_ratio: int

    def __init__(self, unit: MeleeUnit, ratio: int | float):
        self.unit = unit
        self.ratio = ratio

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit: MeleeUnit):
        if unit is not None:
            self._unit = unit

    @property
    def ratio(self):
        return self._spawn_ratio

    @ratio.setter
    def ratio(self, value: int | float):
        if type(value) == int:
            if value < 1:
                self._spawn_ratio = 1
            elif value > 100:
                self._spawn_ratio = 100
            else:
                self._spawn_ratio = value

        elif type(value) == float:
            if value < 0.0:
                self._spawn_ratio = 1
            elif value > 1.0:
                self._spawn_ratio = 100
            else:
                self._spawn_ratio = int(value * 100)
