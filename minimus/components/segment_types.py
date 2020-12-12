# -*- coding: utf-8 -*-

"""Вспомогательный класс для разбора текстового содержимого.
"""
import re
from abc import ABC, abstractmethod
from functools import cached_property
from typing import TypeVar, Generic, Generator

from minimus.utils import markdown_processing
from minimus.utils.output_processing import transliterate

T = TypeVar('T')


class AbstractSegment(Generic[T], ABC):
    """Базовый класс сегментов.
    """

    @abstractmethod
    def __lt__(self, other):
        """Вернуть что то по чему можно будет выполнить сортировку.
        """

    @abstractmethod
    def __str__(self) -> str:
        """Вернуть текстовое представление.
        """

    @classmethod
    @abstractmethod
    def from_string(cls, string: str) -> Generator[T, None, None]:
        """Собрать набор сегментов из строки.
        """


class TextSegment(AbstractSegment):
    """Простой кусок текста.
    """

    def __init__(self, start_outer: int, content: str) -> None:
        """Инициализировать экземпляр.
        """
        self.start_outer = start_outer
        self.content = content
        self.end_outer = self.start_outer + len(content)

    def __str__(self) -> str:
        """Вернуть текстовое представление.
        """
        return self.content

    def __repr__(self) -> str:
        """Вернуть текстовое представление.
        """
        return f'{type(self).__name__}' \
               f'({self.start_outer}, <{self.content!r}>)'

    def __lt__(self, other) -> bool:
        """Сравнить местоположению начала сегмента в строке.
        """
        if hasattr(other, 'start_outer'):
            return self.start_outer < other.start_outer
        return False

    @classmethod
    def from_string(cls, string: str) -> Generator[T, None, None]:
        """Собрать набор сегментов из строки.
        """
        yield cls(0, string)


class RegExSegment(AbstractSegment, ABC):
    """Сегмент на базе регулярного выражения.
    """

    @abstractmethod
    @cached_property
    def inner_text(self) -> str:
        """Вернуть целевой контент сегмента.
        """

    def __init__(self, match: re.Match):
        """Инициализировать экземпляр.
        """
        self.match = match

    def __lt__(self, other) -> bool:
        """Сравнить местоположению начала сегмента в строке.
        """
        if hasattr(other, 'start_outer'):
            return self.start_outer < other.start_outer
        return False

    def __repr__(self) -> str:
        """Вернуть текстовое представление.
        """
        return f'{type(self).__name__}' \
               f'({self.start_inner}, <{self.match.group()}>)'

    @cached_property
    def start_inner(self) -> int:
        """Вернуть индекс, на котором контент начинается в сегменте.
        """
        return self.match.start() + self.match.group().index(self.inner_text)

    @cached_property
    def end_inner(self) -> int:
        """Вернуть индекс, на котором контент заканчивается в сегменте.
        """
        return self.start_inner + len(self.inner_text)

    @cached_property
    def start_outer(self) -> int:
        """Вернуть индекс, на котором сегмент начинается в строке.
        """
        return self.match.start()

    @cached_property
    def end_outer(self) -> int:
        """Вернуть индекс, на котором сегмент заканчивается в строке.
        """
        return self.match.end()


class BareTag(RegExSegment):
    """Голый тег вида '{{ тег }}'.
    """

    def __str__(self) -> str:
        """Вернуть текстовое представление.
        """
        return '[{tag}](./meta_{trans}.md)\n\n'.format(
            tag=self.inner_text,
            trans=transliterate(self.inner_text),
        )

    @cached_property
    def inner_text(self):
        """Вернуть целевой контент сегмента.
        """
        return self.match.group().strip('{} ')

    @classmethod
    def from_string(cls, string: str) -> Generator[T, None, None]:
        """Собрать набор сегментов из строки.
        """
        for match in markdown_processing.extract_bare_tags(string):
            yield cls(match)


class BaseUrl(RegExSegment, ABC):
    """Базовый класс для ссылок.
    """

    def __str__(self) -> str:
        """Вернуть текстовое представление.
        """
        return self.match.group()

    @cached_property
    def inner_text(self):
        """Вернуть целевой контент сегмента.
        """
        return self.match.groups()[0].strip('{} ')


class MarkdownUrl(BaseUrl):
    """Ссылка вида '[название](./file.md)'.
    """

    @classmethod
    def from_string(cls, string: str) -> Generator[T, None, None]:
        """Собрать набор сегментов из строки.
        """
        for match in markdown_processing.extract_full_tags(string):
            yield cls(match)


class Url(BaseUrl):
    """Ссылка вида '[название](http://something)'.
    """

    @classmethod
    def from_string(cls, string: str) -> Generator[T, None, None]:
        """Собрать набор сегментов из строки.
        """
        for match in markdown_processing.extract_urls(string):
            yield cls(match)
