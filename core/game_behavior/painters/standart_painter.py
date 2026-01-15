from ...game_objects.abstract_objects import GameObject


class StandartPainter:
    _objects: list[list[GameObject]] = None
    _mechanic_objects: list[list[GameObject]] = None

    def __init__(self):
        self._objects = []
        self._mechanic_objects = []

    @property
    def objects(self):
        return tuple(self._objects), tuple(self._mechanic_objects)

    @objects.setter
    def objects(self, objects: list[list[GameObject]]):
        self._objects = objects

        for object_list in self._objects:
            if object_list is not None:
                self._sort_collection(object_list)

    def add(self, *objects: GameObject):
        for object_list in objects:
            if object_list is not None:
                self._objects.append(object_list)
                self._sort_collection(object_list)

    def add_debug(self, *objects: GameObject):
        for object_list in objects:
            if object_list is not None:
                self._mechanic_objects.append(object_list)
                self._sort_collection(object_list)

    def paint(self, delta_time: int | float, **kwargs):
        for game_object_list in self._mechanic_objects:
            for game_object in game_object_list:
                game_object.render(delta_time=delta_time, **kwargs)

        for game_object_list in self._objects:
            for game_object in game_object_list:
                game_object.render(delta_time=delta_time, **kwargs)

    def _sort_collection(self, objects: list[GameObject]):
        objects.sort(key=lambda x: x.get_depth())
