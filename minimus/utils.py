# -*- coding: utf-8 -*-

"""Вспомогательные элементы.
"""
from typing import Iterable, Generator, TypeVar

T = TypeVar('T')


def make_prefix(total: int) -> str:
    """Сделать префикс для перечисления

    >>> make_prefix(750)
    '{num:03} из {total:03d}'
    """
    digits = len(str(total))
    prefix = '{{num:0{digits}}} из {{total:0{digits}d}}'.format(digits=digits)
    return prefix


def numerate(collection: Iterable[T]) -> Generator[tuple[str, T], None, None]:
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
