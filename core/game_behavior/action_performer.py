from typing import Callable
from ..game_objects.abstract_objects import GameObject

ObjectPerformer = Callable[[GameObject], None]


class ActionPerformer:
    _objects: list[list[GameObject]]

    _func_performers: list[ObjectPerformer]

    def __init__(self):
        self._objects = []
        self._func_performers = []

    @property
    def performers(self):
        return tuple(self._func_performers)

    @performers.setter
    def performers(
        self,
        performers: ObjectPerformer | list[ObjectPerformer] | tuple[ObjectPerformer],
    ):
        if type(performers) in [list, tuple]:
            self._func_performers.extend(performers)
        else:
            self._func_performers.append(performers)

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
                for func in self._func_performers:
                    func(object_, *args)
