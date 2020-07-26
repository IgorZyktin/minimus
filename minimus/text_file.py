# -*- coding: utf-8 -*-

"""Простая модель для текствого файла.

Не умеет себя сохранять.
Умеет следить за содержимым.
"""
from functools import total_ordering
from typing import Any

from minimus.abstract import AbstractTextFile


@total_ordering
class TextFile(AbstractTextFile):
    """Текстовый файл с произвольным содержимым.
    """
    normal_attrs = {
        'filename',
        'content',
        'is_changed',
        '_filename',
        '_content',
        'attrs',
        'original_content',
        'original_filename'
    }

    def __init__(self, filename: str, content: str, is_changed: bool = False):
        """Инициализировать экземпляр.
        """
        self.original_content = content
        self.original_filename = filename
        self._content = content
        self._filename = filename
        self.is_changed = is_changed
        self.attrs = {}

    def __repr__(self) -> str:
        """Вернуть текстовое представление.
        """
        return '{type}({filename})'.format(
            type=type(self).__name__,
            filename=repr(self.filename),
        )

    def __eq__(self, other):
        """Проверка на равенство.

        Нужна для сортировки по имени, поэтому проверяется только имя.
        """
        if isinstance(other, type(self)):
            return self.filename == other.filename
        return False

    def __lt__(self, other):
        """Проверка, на то, что значение меньше.

        Нужна для сортировки по имени, поэтому проверяется только имя.
        """
        if isinstance(other, type(self)):
            return self.filename < other.filename
        return NotImplemented

    def __hash__(self) -> int:
        """Вернуть хеш по содержимому.
        """
        return hash(self.filename)

    def __getattr__(self, item: str) -> Any:
        """В любой непонятной ситуации мы пытаемся обратиться к attrs.
        """
        value = self.attrs.get(item)

        if value is None:
            raise AttributeError(f'Экземпляр {self} не '
                                 f'имеет атрибута {item}.')
        return value

    def __setattr__(self, key: str, value: Any) -> None:
        """По умолчанию все атрибуты дописываются в attrs.
        """
        if key not in self.normal_attrs:
            self.attrs[key] = value
            return

        object.__setattr__(self, key, value)

    @property
    def filename(self) -> str:
        """Вернуть имя файла.
        """
        return self._filename

    @filename.setter
    def filename(self, new_filename: str) -> None:
        """Изменить имя файла.
        """
        self._filename = new_filename
        self.is_changed = True

    @property
    def content(self) -> str:
        """Вернуть текстовое содержимое файла.
        """
        return self._content

    @content.setter
    def content(self, new_contents: str) -> None:
        """Изменить текстовое содержимое файла.
        """
        self._content = new_contents
        self.is_changed = True
