# -*- coding: utf-8 -*-

"""Translation/transliterations utils.
"""
from typing import Callable, Optional, List, Any

from minimus import settings, constants


def transliterate(something: str) -> str:
    """Make transliteration to a latin charset.

    Used only for filenames.

    >>> transliterate('Два весёлых гуся')
    'dva_veselyh_gusya'
    """
    return something.lower().translate(constants.TRANS_MAP)


def announce(*args: Any, callback: Callable, **kwargs) -> None:
    """Print text but with fancy formatting.

    >>> announce(1, 2, 3, callback=print, z='test')
    1, 2, 3, z=test
    """
    _args = ', '.join(str(x) for x in args)
    text = ', '.join([_args, *to_kv(kwargs)])
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

    if language == 'EN' or language not in constants.VOCABULARY:
        return template

    return constants.VOCABULARY[language].get(template, template)


def to_kv(something: dict) -> List[str]:
    """Break down to key=value pairs.

    >>> to_kv(dict(a=1, b=2))
    ['a=1', 'b=2']
    """
    return [
        f'{key}={value}'
        for key, value in something.items()
    ]
