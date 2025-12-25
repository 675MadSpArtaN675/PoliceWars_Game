from game_objects.abstract_objects import GameObject


class StandartPainter:
    _objects: list[GameObject] = None

    @property
    def objects(self):
        return tuple(self._objects)

    @objects.setter
    def objects(self, objects: list[GameObject]):
        objects_sorted = self._sort_collection(objects)
        self._objects = objects_sorted

    def remove_dead_objects(self):
        self._objects = list(
            self._sort_collection(filter(lambda x: not x.is_dead(), self._objects))
        )

    def paint(self):
        if self._objects is not None:
            for game_object in self._objects:
                game_object.render()

    def _sort_collection(self, objects: list[GameObject]):
        return list(sorted(objects, key=lambda x: x.get_depth()))
