# -*- coding: utf-8 -*-

"""Инструменты работы с Markdown.
"""
from re import Match
from typing import Set, Generator

from minimus import settings


def extract_title(content: str) -> str:
    """Извлечь заголовок из тела документа.
    """
    match = settings.TITLE_PATTERN.match(content)
    if match:
        return match.groups()[0].strip()
    return '???'


def extract_bare_tags(content: str) -> Generator[Match, None, None]:
    """Извлечь все сырые теги из тела документа.
    """
    for match in settings.BARE_TAG_PATTERN.finditer(content):
        yield match


def extract_full_tags(content: str) -> Generator[Match, None, None]:
    """Извлечь все полноразмерные теги из тела документа.
    """
    for match in settings.FULL_TAG_PATTERN.finditer(content):
        yield match


def href(label: str, link: str) -> str:
    """Собрать гиперссылку из частей.

    >>> href('Hello!', 'world')
    '[Hello!](./world)'
    """
    return '[{}](./{})'.format(label, link.lstrip('/'))
