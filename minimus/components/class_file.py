# -*- coding: utf-8 -*-

"""Абстракция файла.

Не занимается работой с файловой системой, берёт на себя только
логику модификации содержимого и отслеживание изменений.
"""
from functools import cached_property, total_ordering
from typing import Dict

from minimus.utils.files_processing import get_ext
from minimus.utils.output_processing import transliterate


class File:
    """Абстракция файла.
    """

    def __init__(self, metainfo_record: Dict[str, str]) -> None:
        """Инициализировать экземпляр.
        """
        self.original_filename = metainfo_record['original_filename']
        self.original_path = metainfo_record['original_path']

        self.title = '???'
        self.is_changed = False
        self.is_saved = False

    def __repr__(self):
        """Вернуть текстовое представление.
        """
        return f'{type(self).__name__}({self.filename})'

    def is_markdown(self) -> bool:
        """Вернуть True если это markdown файл.
        """
        return get_ext(self.original_filename) == 'md'

    @cached_property
    def filename(self) -> str:
        """Вернуть оптимизированное имя файла.
        """
        return transliterate(self.original_filename)

    @cached_property
    def original_content(self) -> str:
        """Вернуть исходное содержимое файла.
        """
        with open(self.original_path, mode='r', encoding='utf-8') as file:
            return file.read()
