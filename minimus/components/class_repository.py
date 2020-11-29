# -*- coding: utf-8 -*-

"""Хранилище абстракций файлов.

Структура исходного и выходного каталога может отличаться, поэтому нам
нужен слой абстракции для исправления путей.
"""

from typing import List, Dict

from minimus.components.class_file import File


class Repository:
    """Хранилище абстракций файлов.
    """

    def __init__(self, metainfo: List[Dict[str, str]]) -> None:
        """Инициализировать экземпляр.
        """
        self._storage_by_filename: Dict[str, File] = {}
        self._storage_by_old_filename: Dict[str, File] = {}

        for record in metainfo:
            file = File(record)
            self._storage_by_filename[file.filename] = file
            self._storage_by_old_filename[file.original_filename] = file

    def __len__(self) -> int:
        """Вернуть число файлов в репозитории.
        """
        return len(self._storage_by_filename)

    def __str__(self) -> str:
        """Вернуть перечень имён.
        """
        names = sorted(self._storage_by_filename)
        return f'{type(self).__name__}({len(names)}, <{names}>)'

    def __iter__(self):
        """Вернуть итератор по файлам.
        """
        return iter(self._storage_by_filename.items())

    def get_files(self) -> List[File]:
        """Вернуть список всех файлов.
        """
        return list(self._storage_by_filename.values())
