# -*- coding: utf-8 -*-

"""Инструменты работы с текстом.
"""
from typing import List, TypeVar, Iterable, Generator, Tuple, Optional

T = TypeVar('T')


def to_kv(something: dict) -> List[str]:
    """Разложить словарь в набор пар ключ=значение.

    >>> to_kv(dict(a=1, b=2))
    ['a=1', 'b=2']
    """
    return [
        f'{key}={value}'
        for key, value in something.items()
    ]


def make_prefix(total: int) -> str:
    """Собрать префикс для нумерации.

    >>> make_prefix(75)
    '{num:02} из {total:02d}'

    >>> make_prefix(750)
    '{num:03} из {total:03d}'
    """
    digits = len(str(total))
    prefix = '{{num:0{0}}} из {{total:0{0}d}}'.format(digits)
    return prefix


def numerate(collection: Iterable[T], total: Optional[int] = None) \
        -> Generator[Tuple[str, T], None, None]:
    """Аналог enumerate, только с красивыми номерами.

    >>> list(numerate(['a', 'b', 'c']))
    [('1 из 3', 'a'), ('2 из 3', 'b'), ('3 из 3', 'c')]
    """
    if total is None:
        collection = list(collection)
        total = len(collection)

    prefix = make_prefix(total)

    for i, each in enumerate(collection, start=1):
        number = prefix.format(num=i, total=total)
        yield number, each
