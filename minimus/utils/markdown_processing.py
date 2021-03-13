# -*- coding: utf-8 -*-

"""Инструменты работы с Markdown.
"""
from re import Match
from typing import Generator

from minimus.utils import regex_patterns


def extract_title(content: str) -> str:
    """Извлечь заголовок из тела документа.
    """
    match = regex_patterns.TITLE_PATTERN.match(content)
    if match:
        return match.groups()[0].strip()
    return '???'


def extract_bare_tags(content: str) -> Generator[Match, None, None]:
    """Извлечь все сырые теги из тела документа.
    """
    for match in regex_patterns.BARE_TAG_PATTERN.finditer(content):
        yield match


def extract_full_tags(content: str) -> Generator[Match, None, None]:
    """Извлечь все полноразмерные теги из тела документа.
    """
    for match in regex_patterns.MARKDOWN_URL_PATTERN.finditer(content):
        yield match


def extract_urls(content: str) -> Generator[Match, None, None]:
    """Извлечь все полноразмерные теги из тела документа.
    """
    for match in regex_patterns.MARKDOWN_URL_PATTERN.finditer(content):
        yield match


def href(label: str, link: str, base_folder: str = './') -> str:
    """Собрать гиперссылку из частей.

    >>> href('Hello!', 'world')
    '[Hello!](./world)'
    """
    if base_folder == '.':
        base_folder = './'

    return '[{}]({})'.format(label, base_folder + link.lstrip('/'))
