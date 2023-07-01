# -*- coding: utf-8 -*-
"""Модуль с классами объектов.
"""
import hashlib
import os
import typing
from functools import cached_property
from pathlib import Path

from minimus import constants


class Fingerprint(typing.TypedDict):
    """Слепок файловой системы, позволяющий определять изменения файлов."""
    md5: str
    created: int
    modified: int
    size: int


class File:
    """Пакет с метаинформацией о файле."""

    def __init__(self, root: Path, path: Path, content: str = '') -> None:
        """Инициализировать экземпляр."""
        self.root = root
        self.path = path
        self._content: str | None = content or None
        self.has_changes = False

    def __eq__(self, other: 'File') -> bool:
        """Вернуть True при равенстве."""
        return self.path == other.path

    def __hash__(self):
        """Вернуть хэш пути."""
        return hash(self.path.absolute())

    @cached_property
    def content(self) -> str:
        """Вернуть содержимое файла."""
        if self._content is None:
            with open(self.path, mode='r', encoding='utf-8') as file:
                self._content = file.read()

        return self._content

    @cached_property
    def fingerprint(self) -> Fingerprint:
        """Вернуть содержимое файла."""
        stat = os.stat(self.path)

        with open(self.path, 'rb') as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        return Fingerprint(
            md5=str(file_hash.hexdigest()),
            created=int(stat.st_ctime),
            modified=int(stat.st_mtime),
            size=stat.st_size,
        )

    @cached_property
    def title(self) -> str:
        """Вернуть заголовок файла."""
        match = constants.TITLE_PATTERN.search(self.content)
        if match is None:
            return constants.UNKNOWN
        return match.groups()[0]

    @cached_property
    def tags(self) -> list[str]:
        """Вернуть все теги в файле."""
        return sorted(
            constants.BASIC_TAG_PATTERN.findall(self.content)
        )
