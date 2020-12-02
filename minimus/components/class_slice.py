# -*- coding: utf-8 -*-

"""Вспомогательный класс для разбора текстового содержимого.
"""
from functools import cached_property
from re import Match

from minimus.utils.output_processing import transliterate

# TODO - терует серьёзной доработки, не рендерит теги внутри документа
class Slice:
    """Сегмент внутри текста.
    """

    def __init__(self, match: Match, full: bool):
        """Инициализировать экземпляр.
        """
        self.match = match
        self.full = full

    def __lt__(self, other):
        if isinstance(self, type(other)):
            return self.start_inner < other.start_inner
        return False

    def __str__(self):
        if self.full:
            return self.match.group()
        return '[<{tag}>](./meta_{trans}.md)' \
            .format(tag=self.inner_text,
                    trans=transliterate(self.inner_text)) \
            .replace('<', '{{').replace('>', '}}')

    def __repr__(self):
        return f'{type(self).__name__}' \
               f'({self.start_inner}, <{self.match.group()}>)'

    @cached_property
    def inner_text(self):
        if self.full:
            return self.match.groups()[0].strip('{} ')
        return self.match.group().strip('{} ')

    @cached_property
    def start_outer(self):
        return self.match.start()

    @cached_property
    def end_outer(self):
        return self.match.end()

    @cached_property
    def start_inner(self):
        return self.match.start() + self.match.group().index(self.inner_text)

    @cached_property
    def end_inner(self):
        return self.start_inner + len(self.inner_text)
