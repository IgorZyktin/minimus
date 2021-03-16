# -*- coding: utf-8 -*-

"""Utils for text processing.
"""
from typing import TypeVar, Iterable, Generator, Tuple, Optional

from minimus.utils.utils_locale import translate as _

T = TypeVar('T')  # pylint: disable=C0103


def make_prefix(total: int, language: str = '') -> str:
    """Make prefix for enumeration.

    >>> make_prefix(75, 'EN')
    '{num:02} of {total:02d}'

    >>> make_prefix(750, 'RU')
    '{num:03} из {total:03d}'
    """
    digits = len(str(total))
    prefix = '{{num:0{digits}}} {sep} {{total:0{digits}d}}'.format(
        sep=_('of', language),
        digits=digits
    )
    return prefix


def numerate(collection: Iterable[T],
             language: str = '', ) -> Generator[Tuple[str, T], None, None]:
    """Same as enumerate, but with fancy numbers.

    >>> list(numerate(['a', 'b', 'c'], language='EN'))
    [('1 of 3', 'a'), ('2 of 3', 'b'), ('3 of 3', 'c')]
    """
    collection = list(collection)
    total = len(collection)
    prefix = make_prefix(total, language)

    for i, each in enumerate(collection, start=1):
        number = prefix.format(num=i, total=total)
        yield number, each
