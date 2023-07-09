"""Утилиты.
"""
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from minimus.src import constants


def make_prefix(total: int) -> str:
    """Сделать префикс для перечисления

    >>> make_prefix(750)
    '{num:03} из {total:03d}'
    """
    digits = len(str(total))
    prefix = '{{num:0{digits}}} из {{total:0{digits}d}}'.format(digits=digits)
    return prefix


T = TypeVar('T')


def numerate(collection: Iterable[T]) -> Iterator[tuple[str, T]]:
    """Проставить номер позиции при перечислении.

    >>> list(numerate(['a', 'b', 'c']))
    [('1 из 3', 'a'), ('2 из 3', 'b'), ('3 из 3', 'c')]
    """
    collection = list(collection)
    total = len(collection)
    prefix = make_prefix(total)

    for i, each in enumerate(collection, start=1):
        number = prefix.format(num=i, total=total)
        yield number, each


def transliterate(something: str) -> str:
    """Конвертировать киррилическое написание в латиницу.

    >>> transliterate('Два весёлых гуся')
    'dva_veselyh_gusya'
    >>> transliterate('regnum dei')
    'regnum_dei'
    """
    return something.lower().translate(constants.TRANS_MAP)
