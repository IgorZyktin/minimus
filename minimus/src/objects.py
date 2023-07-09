"""Модуль с классами объектов.
"""
import hashlib
import json
import os
import typing
from functools import cached_property
from pathlib import Path
from typing import Any

from minimus.src import constants


class Fingerprint(typing.TypedDict):
    """Слепок файловой системы, позволяющий определять изменения файлов."""
    md5: str
    created: int
    modified: int
    size: int


class File:
    """Пакет с метаинформацией о файле."""

    def __init__(
            self,
            path: Path,
            root: Path | None = None,
            content: str | None = None,
    ) -> None:
        """Инициализировать экземпляр."""
        self.root = root or path
        self.path = path
        self._content = content
        self.has_changes = False

    def __eq__(self, other: 'File') -> bool:
        """Вернуть True при равенстве."""
        return self.path == other.path

    def __hash__(self):
        """Вернуть хэш пути."""
        return hash(self.path.absolute())

    def load(self) -> Path:
        """Загрузить содержимое файла."""
        with open(self.path, mode='r', encoding='utf-8') as file:
            self._content = file.read()
        return self.path

    def save(self) -> Path:
        """Сохранить данные об уже обработанных файлах."""
        with open(self.path, mode='w', encoding='utf-8') as file:
            file.write(self.content)
        return self.path

    @property
    def content(self) -> str:
        """Вернуть содержимое файла."""
        if self._content is None:
            self.load()
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        """Установить новое содержимое файла."""
        self._content = new_content

    @cached_property
    def relative_path(self) -> Path:
        """Вернуть путь относительно корня."""
        return self.path.relative_to(self.root)

    @cached_property
    def fingerprint(self) -> Fingerprint:
        """Вернуть слепок файла."""
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


class Cache:
    """Класс для кеша.

    Содержит данные об уже обработанных файлах.
    Позволяет игнорировать их если они не изменялись.
    """

    def __init__(self, path: Path, contents: dict[str, Any]) -> None:
        """Инициализировать экземпляр."""
        self.path = path
        self.contents = contents

    def load(self) -> Path:
        """Загрузить кеш из файла."""
        full_path = self.path / constants.CACHE_FILENAME

        try:
            with open(full_path, mode='r', encoding='utf-8') as file:
                self.contents = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.contents = {}

        return full_path

    def save(self) -> Path:
        """Сохранить данные об уже обработанных файлах."""
        full_path = self.path / constants.CACHE_FILENAME

        with open(full_path, mode='w', encoding='utf-8') as file:
            json.dump(self.contents, file, ensure_ascii=False, indent=4)

        return full_path

    def has_no_changes(self, file: File) -> bool:
        """Вернуть True если файл не менялся с прошлого запуска."""
        return self.contents.get(str(file.path.absolute())) == file.fingerprint

    def store_file(self, file: File) -> None:
        """Обновить данные о файле в кеше."""
        self.contents[str(file.path.absolute())] = file.fingerprint
