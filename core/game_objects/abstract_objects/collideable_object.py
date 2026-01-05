from .game_object import GameObject

import pygame as pg


class CollideableObject(GameObject):
    _restricted_objects: list[type] = ()

    def collision(self, entity: GameObject):
        if type(entity) in self._restricted_objects:
            return False

        sprite = self.get_sprite()
        sprite_enemy = entity.get_sprite()

        return pg.sprite.collide_rect(sprite, sprite_enemy)
