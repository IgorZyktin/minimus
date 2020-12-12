# -*- coding: utf-8 -*-

"""Класс для работы с Markdown. Применяет регулярные выражения к тексту.
"""
from functools import cached_property
from typing import List, Optional, Dict

from minimus.components.segment_types import AbstractSegment
from minimus.utils.markdown_processing import extract_title


class Renderer:
    """Класс для работы с Markdown. Применяет регулярные выражения к тексту.
    """

    def __init__(self, original_content: str) -> None:
        """Инициализировать экземпляр.
        """
        self.original_content = original_content
        self._tags: Dict[str, None] = {}
        self.segments: List[AbstractSegment] = []

    @cached_property
    def title(self) -> str:
        """Вернуть заголовок файла.
        """
        return extract_title(self.original_content)

    def get_tags(self) -> List[str]:
        """Вернуть список тегов в файле.
        """
        return list(self._tags)

    def has_tag(self, tag: str) -> bool:
        """Вернуть True если у нас есть такой тег.
        """
        return tag in self._tags

    @cached_property
    def category(self) -> Optional[str]:
        """Вернуть категорию файла.

        Это первый тег в файле.
        """
        if not self._tags:
            return None

        return list(self._tags)[0]

    def add_tag(self, tag: str) -> None:
        """Добавить тег в перечнь тегов.

        Нам надо сохранять теги без дубликатов, но хранить порядок вставки.
        """
        if not self.has_tag(tag):
            self._tags[tag] = None

    @cached_property
    def content(self) -> str:
        """Вернуть итоговое содержимое файла.
        """
        return ''.join(map(str, self.segments))
