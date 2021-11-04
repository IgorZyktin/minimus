# -*- coding: utf-8 -*-

"""Модуль c классами объектов.
"""
import os
import typing
from dataclasses import dataclass
from functools import cached_property


class Fingerprint(typing.TypedDict):
    """Слепок файловой системы, позволяющий определять изменения файлов."""
    md5: str
    created: int
    modified: int
    size: int


@dataclass
class Pointer:
    """Пакет с метаинформацией о файле."""
    path: str
    filename: str
    steps: tuple[str, ...]
    fingerprint: Fingerprint

    @cached_property
    def location(self) -> str:
        """Вернуть локальный путь."""
        return os.path.join(*self.steps, self.filename)


@dataclass
class Warning:
    lines: list[str]


@dataclass
class Document:
    """Эквивалент одной заметки."""
    pointer: Pointer
    title: str
    header: str
    tags: list[str]
    body: str
    warnings: list[Warning]
    rendered: str = ''


@dataclass
class Tag:
    """Эквивалент одного тега."""
    title: str
    filename: str
    rendered: str = ''


class Correspondence:
    """Соответствие тегов и документов."""

    def __init__(self):
        """Инициализировать экземпляр."""
        self.tags_to_documents: dict[tuple[str, str], list[Document]] = {}
        self.tags_to_tags: dict[tuple[str, str], set[str]] = {}

    def add_tag(self, tag: str, document: Document) -> None:
        """Добавить тег в хранилище."""
        pair = tag, tag.casefold()

        if pair in self.tags_to_documents:
            self.tags_to_documents[pair].append(document)
        else:
            self.tags_to_documents[pair] = [document]

        if pair in self.tags_to_tags:
            self.tags_to_tags[pair].update(document.tags)
        else:
            self.tags_to_tags[pair] = set(document.tags)
