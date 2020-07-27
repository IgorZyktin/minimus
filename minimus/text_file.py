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

    def __init__(self, filename: str, content: str,
                 is_changed: bool = False, **kwargs):
        """Инициализировать экземпляр.
        """
        self.original_content = content
        self.original_filename = filename
        self._content = content
        self._filename = filename
        self.is_changed = is_changed
        self.attrs = {**kwargs}

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
        item = item.lower()

        value = self.attrs.get(item)

        if value is None:
            raise AttributeError(f'Экземпляр {self} не '
                                 f'имеет атрибута {item}.')
        return value

    def __setattr__(self, key: str, value: Any) -> None:
        """По умолчанию все атрибуты дописываются в attrs.
        """
        key = key.lower()

        if key == 'contents':
            raise NameError(f'Атрибут {type(self).__name__} с текстовым '
                            f'содержимым должен называться "content", '
                            f'а не "contents".')

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
        if new_filename != self._filename:
            self.is_changed = True
        self._filename = new_filename

    @property
    def content(self) -> str:
        """Вернуть текстовое содержимое файла.
        """
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        """Изменить текстовое содержимое файла.
        """
        if new_content != self._content:
            self.is_changed = True
        self._content = new_content
