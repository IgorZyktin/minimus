# -*- coding: utf-8 -*-

"""Хранилище абстракций файлов.

Структура исходного и выходного каталога может отличаться, поэтому нам
нужен слой абстракции для исправления путей.
"""

from typing import Dict

from minimus.components.class_file import File
from minimus.utils.files_processing import read_text
from minimus.components.class_meta import Meta


class Repository:
    """Хранилище абстракций файлов.
    """

    def __init__(self, metainfo: Dict[str, Meta],
                 stored_metainfo: Dict[str, Meta]) -> None:
        """Инициализировать экземпляр.
        """
        self.metainfo = metainfo
        self.stored_metainfo = stored_metainfo

        self._storage_by_filename: Dict[str, File] = {}
        self._storage_by_old_filename: Dict[str, File] = {}

    def __len__(self) -> int:
        """Вернуть число файлов в репозитории.
        """
        return len(self._storage_by_filename)

    def __str__(self) -> str:
        """Вернуть перечень имён.
        """
        names = sorted(self._storage_by_filename.keys())
        return f'{type(self).__name__}({len(names)}, <{names}>)'

    def __iter__(self):
        """Вернуть итератор по файлам.
        """
        return iter(self._storage_by_filename.values())

    def create_files(self) -> None:
        """Произвести сборку экземпляров файлов из метаинформации.
        """
        for original_filename, meta in self.metainfo.items():
            stored_meta = self.stored_metainfo.get(original_filename)
            file = File(meta=meta, stored_meta=stored_meta)
            self._storage_by_filename[file.meta.filename] = file
            self._storage_by_old_filename[original_filename] = file

    def read_contents_from_disk(self) -> None:
        """Прочитать содержимое изменённых файлов с диска.
        """
        for file in self._storage_by_filename.values():
            if file.is_markdown() and file.is_updated:
                file.original_content = read_text(
                    path=file.meta.original_path,
                    filename=file.meta.original_filename,
                ),
