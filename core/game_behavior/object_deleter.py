from ..game_objects.abstract_objects import GameObject


class ObjectDeleter:
    _objects: list[list[GameObject]]

    def __init__(self):
        self._objects = []

    @property
    def objects(self):
        return tuple(self._objects)

    @objects.setter
    def objects(self, value: list[list[GameObject]]):
        self._objects = value

    def add(self, *objects: list[GameObject]):
        for object_list in objects:
            self._objects.append(object_list)

    def remove_dead_objects(self):
        for object_list in self._objects:
            for object_ in object_list:
                if object_.is_dead():
                    del object_list[object_list.index(object_)]
