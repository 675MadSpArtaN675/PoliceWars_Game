from game_objects.abstract_objects import GameObject


class StandartPainter:
    _objects: list[list[GameObject]] = None

    def __init__(self):
        self._objects = []

    @property
    def objects(self):
        return tuple(self._objects)

    @objects.setter
    def objects(self, objects: list[GameObject]):
        self._objects = objects
        self._sort_collection(self._objects)

    def add(self, *objects: GameObject):
        for object_list in objects:
            if object_list is not None:
                self._objects.append(object_list)
                self._sort_collection(object_list)

    def paint(self):
        for game_object_list in self._objects:
            for game_object in game_object_list:
                game_object.render()

    def _sort_collection(self, objects: list[GameObject]):
        objects.sort(key=lambda x: x.get_depth())
