from .game_object import GameObject

import pygame as pg

import copy


class CollideableObject(GameObject):
    _is_ghost_object: bool = False
    _restricted_objects: list[type] = ()

    def collision(self, entity: GameObject):
        if type(entity) in self._restricted_objects or entity._is_ghost_object:
            return False

        sprite = self.get_sprite()
        sprite_enemy = entity.get_sprite()

        return pg.sprite.collide_rect(sprite, sprite_enemy)

    def __deepcopy__(self, memo: dict[int, object]):
        object_copy = super().__deepcopy__(memo)

        object_copy._is_ghost_object = self._is_ghost_object
        object_copy._restricted_objects = self._copy_linked_objects(
            self._restricted_objects
        )

        return object_copy
