from utility_classes.size import Size

from ...game_objects.abstract_objects import GameObject

from .standart_painter import StandartPainter


class ObjectPainter(StandartPainter):
    _policmans_field_size: Size = None

    _background_objects: list[GameObject] = None

    @property
    def field_size(self):
        return self._policmans_field_size

    @field_size.setter
    def field_size(self, size: Size):
        self._policmans_field_size = size

    def paint_background(self, delta_time: int | float):
        if (
            self._policmans_field_size is not None
            and self._background_objects is not None
        ):
            for background_object in self._background_objects:
                background_object.render(delta_time)
