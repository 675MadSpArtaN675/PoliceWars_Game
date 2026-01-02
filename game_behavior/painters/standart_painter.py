from game_objects.abstract_objects import GameObject


class StandartPainter:
    _objects: list[GameObject] = None

    def __init__(self):
        self._objects = []

    @property
    def objects(self):
        return tuple(self._objects)

    @objects.setter
    def objects(self, objects: list[GameObject]):
        self._objects = objects
        self._sort_collection(self._objects)

    def add(self, object_: GameObject):
        if object_ is not None:
            self._objects.append(object_)
            self._objects = self._sort_collection(self._objects)

    def remove_dead_objects(self):
        if self._objects is not None:
            self._remove_dead_objects(self._objects)

    def _remove_dead_objects(self, objects: list[GameObject]):
        for object_ in objects:
            if object_.is_dead():
                objects.remove(object_)

    def paint(self):
        if self._objects is not None:
            for game_object in self._objects:
                game_object.render()

    def _sort_collection(self, objects: list[GameObject]):
        objects.sort(key=lambda x: x.get_depth())
