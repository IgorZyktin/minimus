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

    render_html = False

    _base_path = Path().absolute()
    launch_directory = _base_path
    script_directory = _base_path
    source_directory = _base_path
    target_directory = _base_path

    html_template = ''

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
        for key in dir(self):
            value = getattr(self, key, None)
            if any(['__' in key,
                    key.isupper(),
                    callable(value),
                    key.startswith('_')]):
                continue

            pairs.append(f'{key}={value!r}')

        type_name = type(self).__name__
        prefix = f'{type_name}(\n'
        body = ['    ' + x for x in sorted(pairs)]
        return prefix + ',\n'.join(body) + '\n)'
