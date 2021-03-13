# -*- coding: utf-8 -*-

"""Инструменты работы с текстовым выводом для пользователя.
"""
from typing import Callable, Optional, List

from minimus import settings
from minimus import contants


def transliterate(something: str) -> str:
    """Make transliteration to a latin charset.

    Used only for filenames.

    >>> transliterate('Два весёлых гуся')
    'dva_veselyh_gusya'
    """
    return something.lower().translate(contants.TRANS_MAP)


def announce(*args, callback: Callable, **kwargs) -> None:
    """Print text but with fancy formatting.

    >>> announce(1, 2, 3, callback=print, z='test')
    1, 2, 3, z=test
    """
    args = ', '.join(map(str, args))
    text = ', '.join([args, *to_kv(kwargs)])
    callback(text)


def stdout(template: str, *args, callback: Optional[Callable] = None,
           language: Optional[str] = None, color: str = '', **kwargs):
    """Print text on screen in specified user language."""
    template = translate(template, language=language or settings.LANGUAGE)
    text = color + template.format(**kwargs)
    announce(text, *args, callback=callback or print)


def translate(template: str, language: str = '') -> str:
    """Translate text to a specific language.

    >>> translate('hello world', 'RU')
    'привет мир'
    """
    if not language:
        language = settings.LANGUAGE

    if language == 'EN' or language not in contants.VOCABULARY:
        return template

    return contants.VOCABULARY[language].get(template, template)


def to_kv(something: dict) -> List[str]:
    """Break down to key=value pairs.

    >>> to_kv(dict(a=1, b=2))
    ['a=1', 'b=2']
    """
    return [
        f'{key}={value}'
        for key, value in something.items()
    ]
