from typing import Callable
from game_objects.abstract_objects import GameObject


class ActionPerformer:
    _objects: list[list[GameObject]]

    func_performer: Callable[[GameObject], None]

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

    def perform(self, *args):
        for object_list in self._objects:
            for object_ in object_list:
                self.func_performer(object_, *args)

    def remove_dead_objects(self):
        for object_list in self._objects:
            for object_ in object_list:
                if object_ is not None and object_.is_dead():
                    self._objects.remove(object_)
