# -*- coding: utf-8 -*-

"""Инструменты работы с файловой системой.
"""
import json
import os
from dataclasses import dataclass
from typing import List

from minimus.utils.filesystem import join
from minimus.utils.output_processing import translate


@dataclass
class SummaryRecord:
    """Контейнер для данных о файле.
    """
    original_filename: str
    original_path: str
    stat: os.stat_result

    def __repr__(self):
        """Вернуть текстовое представление.
        """
        return f'{type(self).__name__}(<{self.original_filename}>)'


def get_summary(source_directory: str, language: str) -> List[SummaryRecord]:
    """Собрать плоский список всего, что есть в source_directory.

    Каталоги игнорируются.
    """
    if not os.path.exists(source_directory):
        return []

    metainfo = []

    for path, _, filenames in os.walk(source_directory):
        for filename in filenames:
            if filename in metainfo:
                raise FileExistsError(translate(
                    'Filenames are supposed to be unique: {filename}',
                    language=language,
                ))

            full_path = join(path, filename)
            new_record = SummaryRecord(
                original_filename=filename,
                original_path=os.path.abspath(full_path),
                stat=os.stat(full_path),
            )
            metainfo.append(new_record)

    return metainfo


def get_metainfo(source_directory: str, metafile_name: str) -> dict:
    """Попытаться загрузить метаинформацию с прошлого запуска.
    """
    path = join(source_directory, metafile_name)

    try:
        with open(path, mode='r', encoding='utf-8') as file:
            metainfo = json.load(file)
    except FileNotFoundError:
        metainfo = {}

    return metainfo


# def write_text(path: str, filename: str, content: str) -> str:
#     """Сохранить некий текст под определённым именем на диск.
#     """
#     if not content:
#         return ''
#
#     ensure_folder_exists(path)
#     full_path = join_path(path, filename)
#
#     with open(full_path, mode='w', encoding='utf-8') as file:
#         file.write(content)
#
#     return full_path
