# -*- coding: utf-8 -*-

"""Специальный класс для работы с текстом.
"""
import json
from typing import TypeVar, List, Callable, Generator, Tuple, Iterable

T = TypeVar('T')


class Syntax:
    """Мастер по манипуляциям с любым текстом.
    """
    _small_letters = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ъ': '',
        'ы': 'y',
        'ь': '',
        'э': 'e',
        'ю': 'y',
        'я': 'ya',
        ' ': '_',
    }
    _big_letters = {
        key.upper(): value.upper()
        for key, value in _small_letters.items()
    }
    _trans_map = str.maketrans(
        {
            **_small_letters,
            **_big_letters
        }
    )

    @classmethod
    def transliterate(cls, something: str) -> str:
        """Выполнить транслитерацию из кириллицы.

        Используется только для имён файлов и
        не предполагает сложности обработки.

        >>> Syntax.transliterate('Два весёлых гуся')
        'dva_veselyh_gusya'
        """
        return something.lower().translate(cls._trans_map)

    @staticmethod
    def to_kv(something: dict) -> List[str]:
        """Разложить словарь в набор пар ключ=значение.
        """
        return [
            f'{key}={value}'
            for key, value in something.items()
        ]

    @classmethod
    def announce(cls, *args, callback: Callable = print, **kwargs) -> None:
        """Вывод для пользователя.
        """
        args = ', '.join(map(str, args))
        callback(', '.join([args, *cls.to_kv(kwargs)]))

    @staticmethod
    def make_prefix(total: int) -> str:
        """Собрать префикс для нумерации.
        """
        digits = len(str(total))
        prefix = '{{num:0{0}}} из {{total:0{0}d}}'.format(digits)
        return prefix

    @classmethod
    def numerate(cls, collection: Iterable[T]) \
            -> Generator[Tuple[str, T], None, None]:
        """Аналог enumerate, только с красивыми номерами.
        """
        collection = list(collection)
        total = len(collection)
        prefix = cls.make_prefix(total)

        for i, each in enumerate(collection, start=1):
            number = prefix.format(num=i, total=total)
            yield number, each

    @staticmethod
    def to_json(something: dict, indent: int = 4) -> str:
        """Преобразовать словарь в JSON строку.
        """
        return json.dumps(something, ensure_ascii=False, indent=indent)
