from ..sprites_types import (
    SimpleSprite,
    Animator,
)

from ..sprites_types.data import ImageOptions, SpriteType

from utility_classes import Size

import pygame as pg


class ImageParser:
    _size: Size = None
    _time_between_frame: int | float = 0

    def __init__(self, standart_sprite_size: Size, time_between_frame: int | float):
        self._size = standart_sprite_size
        self._time_between_frame = time_between_frame

    def parse_images(self, configs: list[ImageOptions]):
        if len(configs) <= 0:
            return []

        configs_dict = {}
        history = []

        index = 0
        while index < len(configs):
            config = configs[index]
            config_name = config.name

            if config.sprite_type == SpriteType.Animated and config_name not in history:
                filter_frames = tuple(
                    filter(lambda sprite: sprite.name == config_name, configs)
                )

                if len(filter_frames) > 0:
                    sorted_frames = sorted(
                        filter_frames, key=lambda frame: frame.get_frame_num()
                    )
                    sprite_list = [self.parse_image(frame) for frame in sorted_frames]

                    configs_dict[config_name + "_anim"] = Animator(
                        sprite_list[0].rect.width,
                        sprite_list[0].rect.height,
                        self._time_between_frame,
                        sprite_list,
                    )

            else:
                configs_dict[config_name] = self.parse_image(config)

            index += 1

        return configs_dict

    def parse_image(self, image_config: ImageOptions):
        texture = image_config.get_image()
        size = (
            Size(texture.get_rect().width, texture.get_rect().height)
            * image_config.scale.to_tuple()
        )

        scaled_texture = pg.transform.scale(texture, size.to_tuple())
        image_config.set_image(scaled_texture)

        rect = scaled_texture.get_rect()
        source_position = rect.x, rect.y
        image_config.set_source_size(source_position)

        return SimpleSprite(*self._size.to_tuple(), data=image_config)
