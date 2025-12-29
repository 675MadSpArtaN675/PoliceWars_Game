from typing import Callable
from game_objects.abstract_objects import GameObject


class ActionPerformer:
    _objects: list[GameObject]

    func_performer: Callable[[GameObject], None]

    def __init__(self):
        self._objects = []

    @property
    def objects(self):
        return tuple(self._objects)

    @objects.setter
    def objects(self, value: list[GameObject]):
        self._objects = value

    def perform(self, *args):
        for object_ in self._objects:
            self.func_performer(object_, *args)

    def remove_dead_objects(self):
        for object_ in self._objects:
            if object_.is_dead():
                self._objects.remove(object_)
