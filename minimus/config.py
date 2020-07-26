# -*- coding: utf-8 -*-

"""Специальный класс для хранения настроек.
"""
from pathlib import Path


class Config:
    """Специальный класс для хранения настроек.
    """
    lang = 'RU'
    bg_color_tag = '#04266c'
    bg_color_node = '#5a0000'
    protocol = 'file://'

    __BASE_PATH = Path().absolute()
    launch_directory = __BASE_PATH
    script_directory = __BASE_PATH
    source_directory = __BASE_PATH
    target_directory = __BASE_PATH

    custom_source = False
    custom_target = False

    def __repr__(self) -> str:
        """Вернуть текстовое представление.
        """
        return type(self).__name__ + '()'

    def __str__(self) -> str:
        """Вернуть текстовое представление.
        """
        pairs = []
        for key, value in vars(self).items():
            if any([
                '__' in key,
                key.isupper(),
                callable(value)
            ]):
                continue

            pairs.append(f'{key}={value!r}')

        name = type(self).__name__
        return f'{name}(' + ', '.join(pairs) + ')'
