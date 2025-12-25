from utility_classes.size import Size
from game_objects.abstract_objects import GameObject
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

    def add(self, object_: GameObject):
        if object_ is not None:
            self._objects.append(object_)
            self._objects = self._sort_collection(self._objects)

    def remove_dead_objects(self):
        super().remove_dead_objects()

        self._background_objects = list(
            self._sort_collection(
                filter(lambda x: not x.is_dead(), self._background_objects)
            )
        )

    def paint_background(self):
        if (
            self._policmans_field_size is not None
            and self._background_objects is not None
        ):
            for background_object in self._background_objects:
                background_object.render()
