# -*- coding: utf-8 -*-

"""Модуль анализа исходного текста заметок.
"""
import re

import minimus.objects
from minimus import objects, render


def make_documents(notes_with_text: list[tuple[minimus.objects.Pointer, str]]
                   ) -> list[objects.Document]:
    """Преобразовать исходных текст в экземпляры документа."""
    documents = []

    for pointer, text in notes_with_text:
        title, header, tags, body = split_text(text, pointer)
        new_document = objects.Document(
            pointer=pointer,
            title=title,
            header=header,
            tags=tags,
            body=body,
            warnings=check_text(pointer, text),
        )
        documents.append(new_document)

    return documents


def split_text(text: str,
               pointer: objects.Pointer) -> tuple[str, str, list[str], str]:
    """Разделить исходный текст документа на секции."""
    segments = [x.strip() for x in text.split('---', maxsplit=2)]

    if len(segments) != 3:
        raise ValueError(
            'Minimus предполагает, что документ будет '
            f'состоять из заголовка, тегов и собственно '
            f'текста, а у {pointer.location} это не так'
        )

    try:
        raw_header, raw_tags, body = segments
        title, header = split_header(raw_header)
        tags = split_tags(raw_tags)
    except Exception:
        raise ValueError(
            f'Не удалось обработать документ {pointer.location}'
        )

    return title, header, tags, body


def split_header(raw_header: str) -> tuple[str, str]:
    """Разделить сырую шапку на заголовок и собственно шапку."""
    first, *rest = [x.strip() for x in raw_header.split('\n', maxsplit=1)]
    return first.strip('# '), ''.join(rest)


def split_tags(raw_tags: str) -> list[str]:
    """Выделить теги из текста."""
    _, *rest = [x.strip('-* ') for x in raw_tags.split('\n')]
    return [x for x in rest if x]


LINK_PATTERN = re.compile(r'\[.+\]\s*\((.+)\)')


def check_text(pointer: minimus.objects.Pointer, text: str) -> list[Warning]:
    """Подготовить предупреждения если с текстом что то не так."""
    warnings = []
    for link in LINK_PATTERN.finditer(text):
        url = link.groups()[0]
        escaped_url = render.escape(url)
        if url != escaped_url:
            new_warning = objects.Warning([
                f'Рекомендуемся изменить '
                f'ссылку в документе {pointer.location}',
                f'C варианта: {url}',
                f'На вариант: {escaped_url}',
            ])
            warnings.append(new_warning)

    return warnings


def extract_warnings(documents: list[objects.Document]) -> list[str]:
    """Извлечь все предупреждения."""
    lines = []
    for document in documents:
        for warning in document.warnings:
            lines.extend(warning.lines)
    return lines
