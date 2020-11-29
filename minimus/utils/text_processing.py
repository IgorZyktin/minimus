# -*- coding: utf-8 -*-

"""Инструменты работы с текстом.
"""
from typing import List, TypeVar, Iterable, Generator, Tuple


def to_kv(something: dict) -> List[str]:
    """Разложить словарь в набор пар ключ=значение.

    >>> to_kv(dict(a=1, b=2))
    ['a=1', 'b=2']
    """
    return [
        f'{key}={value}'
        for key, value in something.items()
    ]


T = TypeVar('T')


def make_prefix(total: int) -> str:
    """Собрать префикс для нумерации.
    """
    digits = len(str(total))
    prefix = '{{num:0{0}}} из {{total:0{0}d}}'.format(digits)
    return prefix


def numerate(collection: Iterable[T]) \
        -> Generator[Tuple[str, T], None, None]:
    """Аналог enumerate, только с красивыми номерами.
    """
    collection = list(collection)
    total = len(collection)
    prefix = make_prefix(total)

    for i, each in enumerate(collection, start=1):
        number = prefix.format(num=i, total=total)
        yield number, each
