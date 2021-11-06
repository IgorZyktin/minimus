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

    @cached_property
    def location_url(self) -> str:
        """Вернуть локальный путь(для гиперссылки)."""
        return '/'.join([*self.steps, self.filename])


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

    def __repr__(self) -> str:
        """Вернуть текстовое представление."""
        return f'<Document("{self.pointer.filename}")>'


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
        self.tags_to_documents: dict[str, list[Document]] = {}
        self.tags_to_tags: dict[str, set[str]] = {}
        self.casefold_to_normal: dict[str, str] = {}

    def add_tag(self, tag: str, document: Document) -> None:
        """Добавить тег в хранилище."""
        key = self._add_tag_variant(tag)

        if key in self.tags_to_documents:
            self.tags_to_documents[key].append(document)
        else:
            self.tags_to_documents[key] = [document]

        if key in self.tags_to_tags:
            self.tags_to_tags[key].update(document.tags)
        else:
            self.tags_to_tags[key] = set(document.tags)

    def _add_tag_variant(self, tag: str) -> str:
        """Сохранить не зависящий от регистра вариант тега.

        С одной стороны не хочется менять форматирование пользователя,
        с другой хотелось бы отдать предпочтение тегам с заглавной буквы.
        Мы будем стараться хранить в качестве рабочей версии вариант
        написания с первой заглавной буквой.
        """
        independent = tag.casefold()

        saved = self.casefold_to_normal.get(independent)
        if saved and tag:
            first_letter_saved_is_not_upper = saved[0] != saved[0].upper()
            first_letter_tag_is_upper = tag[0] == tag[0].upper()
            if first_letter_saved_is_not_upper and first_letter_tag_is_upper:
                self.casefold_to_normal[independent] = tag
        else:
            self.casefold_to_normal[independent] = tag

        return independent
