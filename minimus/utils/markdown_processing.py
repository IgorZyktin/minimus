# -*- coding: utf-8 -*-

"""Инструменты работы с Markdown.
"""
from collections import defaultdict
from itertools import chain
from typing import List, Dict, Set

from minimus import settings
from minimus.components.class_file import File


def map_tags_to_files(files: List[File]) -> Dict[str, List[File]]:
    """Собрать отображение тегов на файлы.

    Пример вывода:
    {
        '4 лапы':
            [
                File('2020-07-06_elephant.md'),
                File('2020-07-06_mouse.md')
            ],
        'серый':
            [
                File('2020-07-06_elephant.md'),
                File('2020-07-06_mouse.md')
            ],
    }
    """
    tags_to_files = defaultdict(list)

    for file in files:
        if file.is_markdown():
            file.title = extract_title(file.original_content)

            tags = extract_tags(file.original_content)
            bare_tags = extract_bare_tags(file.original_content)

            for tag in chain(tags, bare_tags):
                tags_to_files[tag].append(file)

    return {
        tag: files
        for tag, files in tags_to_files.items()
    }


def extract_title(content: str) -> str:
    """Извлечь заголовок из тела документа.
    """
    match = settings.TITLE_PATTERN.match(content)
    if match:
        return match.groups()[0].strip()
    return '???'


def extract_tags(content: str) -> Set[str]:
    """Извлечь все теги из тела документа.
    """
    all_tags = set()

    for full_tag in settings.FULL_TAG_PATTERN.finditer(content):
        tag_text, _ = full_tag.groups()
        all_tags.add(tag_text)

    return normalize_tags(all_tags)


def extract_bare_tags(content: str) -> Set[str]:
    """Извлечь все сырые теги из тела документа.
    """
    tags = set(settings.HEAD_BARE_TAG_PATTERN.findall(content))
    return normalize_tags(tags)


def normalize_tags(tags: Set[str]) -> Set[str]:
    """Привести все теги к похожему написанию
    """
    return {x.lower().strip() for x in tags}
