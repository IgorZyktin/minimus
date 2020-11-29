# -*- coding: utf-8 -*-

"""Инструменты работы с файловой системой.
"""
import os
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from minimus.utils.output_processing import stdout


@contextmanager
def safe_operation():
    """Контекстный менеджер для вывода сообщений пользователю.

    Пользователь может быть ни разу не программистом, так что
    не стоит вываливать ему простой трейсбек.
    """
    try:
        yield
    except Exception as err:
        # TODO
        print(err)


def make_metainfo(source_directory: str) -> List[dict]:
    """Собрать плоский список всего, что есть в source_directory.

    Каталоги игнорируются.
    """
    if not os.path.exists(source_directory):
        return []

    metainfo = []

    for path, _, filenames in os.walk(source_directory):
        for filename in filenames:
            full_path = os.path.join(path, filename)
            new_record = {
                'original_filename': filename,
                'original_path': os.path.abspath(full_path),
            }
            metainfo.append(new_record)

    return metainfo


def ensure_folder_exists(path: str) -> Optional[str]:
    """Создать всю цепочку каталогов для указанного пути.

    Вернуть путь, если каталог был создан.
    Нельзя давать этой функции имена файлов!
    """
    path = Path(path)
    parts = list(path.parts)
    current_path = None

    for part in parts:
        if current_path is None:
            current_path = part
        else:
            current_path = os.path.join(current_path, part)

        if not os.path.exists(current_path):
            with safe_operation():
                os.mkdir(current_path)
                stdout(
                    'New folder has been created: "{folder}"',
                    folder=current_path,
                )

    return current_path


def get_ext(filename: str) -> str:
    """Вернуть расширение файла.

    >>> get_ext('something.txt')
    'txt'
    """
    _, ext = os.path.splitext(filename.lower())
    return ext.lstrip('.')
