from game_objects.units import MeleeUnit

from functools import partial


class UnitChooser:
    _buffer: MeleeUnit = None
    _chosen_unit_types: list[MeleeUnit] = ()

    def __init__(self, chosen_units: list[MeleeUnit]):
        self._chosen_unit_types = chosen_units

    @property
    def available_units(self):
        return self._chosen_unit_types

    def get_setter_functions(self):
        return [
            partial(self.choose_unit, index)
            for index in range(len(self._chosen_unit_types))
        ]

    def choose_unit(self, index: int):
        self._buffer = self._chosen_unit_types[index]

    def extract_unit(self):
        if self._buffer is not None:
            unit_type = self._buffer.copy()
            self._buffer = None

            return unit_type
