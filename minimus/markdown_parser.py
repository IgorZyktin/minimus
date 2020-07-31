# -*- coding: utf-8 -*-

"""Класс для работы с форматом Markdown.
"""
import re
from typing import Set, Type

from minimus.abstract import AbstractDocument


class MarkdownParser:
    """Класс для работы с форматом Markdown.

    TITLE_PATTERN - шаблон заголовка
        Произвольное количество пробелов от начала строки, за которыми следуют
        один или несколько октоторпов. Потом идёт обязательный пробел (одно из
        отличий заголовка от тега), за которым произвольный набор символов
        до конца строки.

    HEAD_BARE_TAG_PATTERN - шаблон голого тега из заголовка статьи.
        Это тег, который ещё не был отформатирован пользователем.
        Строго с начала строки, затем экранированный октоторп и
        сразу текст без пробела, считываемый до конца строки.

    BODY_BARE_TAG_PATTERN - неотформатированный тег, но уже в теле документа.
        Мы заведомо не знаем, где кончается текст тега, так что этот
        шаблон надо по месту достравивать для каждого тега.

    FULL_TAG_PATTERN - отформатированный тег в теле документа.
        Он уже оформлен в виде гиперссылки.
    """

    TITLE_PATTERN = re.compile(r'^\s*#+\s(.*)', flags=re.MULTILINE)
    HEAD_BARE_TAG_PATTERN = re.compile(r'^\\#(.*)$', flags=re.MULTILINE)
    FULL_TAG_PATTERN = re.compile(r'\[\\#(.*)\]\(\./(.*.md)\)')

    HEAD_BARE_TAG_PATTERN_CUSTOM = r'^\\#{}$'
    BODY_BARE_TAG_PATTERN_CUSTOM = r'(?<!\[)\\#({})(?!\])'

    @staticmethod
    def href(label: str, link: str) -> str:
        """Собрать гиперссылку из частей.

        >>> MarkdownParser.href('Hello!', 'world')
        '[Hello!](./world)'
        """
        return '[{}](./{})'.format(label, link.lstrip('/'))

    @classmethod
    def tag2href(cls, text: str, maker: Type[AbstractDocument]) -> str:
        """Конверсия в гиперссылку.
        """
        link = maker.make_corresponding_filename(text)
        return cls.href(r'\#' + text, link)

    @classmethod
    def extract_title(cls, content: str) -> str:
        """Извлечь заголовок из тела документа.
        """
        match = cls.TITLE_PATTERN.match(content)
        if match:
            return match.groups()[0].strip()
        return '???'

    @classmethod
    def extract_tags(cls, content: str) -> Set[str]:
        """Извлечь все теги из тела документа.
        """
        all_tags = set()
        bare_tags = set()

        for each in cls.HEAD_BARE_TAG_PATTERN.findall(content):
            bare_tags.add(each)
            all_tags.add(each)

        for each in bare_tags:
            sub_pattern = cls.BODY_BARE_TAG_PATTERN_CUSTOM.format(each)
            for sub_tag in re.findall(sub_pattern, content):
                all_tags.add(sub_tag)

        for full_tag in cls.FULL_TAG_PATTERN.finditer(content):
            tag_text, _ = full_tag.groups()
            all_tags.add(tag_text)

        return {
            x.lower().strip()
            for x in all_tags
        }

    @classmethod
    def replace_tags_with_hrefs(cls, content: str, tags: Set[str],
                                maker: Type[AbstractDocument]) -> str:
        """Перестроить текст так, чтобы теги стали гиперрсылками.
        """
        for tag in cls.HEAD_BARE_TAG_PATTERN.findall(content):
            sub_pattern = cls.HEAD_BARE_TAG_PATTERN_CUSTOM.format(tag)
            content = re.sub(sub_pattern, cls.tag2href(tag, maker), content)

        for tag in tags:
            sub_pattern = cls.BODY_BARE_TAG_PATTERN_CUSTOM.format(tag)
            content = re.sub(sub_pattern, cls.tag2href(tag, maker), content)

        return content
