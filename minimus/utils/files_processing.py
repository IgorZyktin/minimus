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
            full_path = join_path(path, filename)
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
            current_path = join_path(current_path, part)

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


def join_path(path: str, filename: str) -> str:
    """Сшить путь с именем файла.
    """
    return os.path.join(path, filename)


def write_text(path: str, filename: str, content: str) -> str:
    """Сохранить некий текст под определённым именем на диск.
    """
    if not content:
        return ''

    ensure_folder_exists(path)
    full_path = join_path(path, filename)

    with open(full_path, mode='w', encoding='utf-8') as file:
        file.write(content)

    return full_path


def shortest_common_path(readme_directory: str, target_directory: str) -> str:
    """Собрать минимально возможный по длине относительный путь из двух путей.

    >>> shortest_common_path(r"C:\\usr\\va", r"C:\\usr\\bg\\doc\\pictures\\ew")
    '..\\bg\\doc\\pictures\\ew'
    """
    if readme_directory == target_directory:
        return '.'

    head_parts = list(Path(readme_directory).parts)
    tail_parts = list(Path(target_directory).parts)

    common_elements = 0

    while head_parts and tail_parts:
        if head_parts[0] != tail_parts[0]:
            break

        head_parts.pop(0)
        tail_parts.pop(0)
        common_elements += 1

    if not common_elements:
        return target_directory

    resulting_path = ''

    if head_parts:
        for _ in head_parts:
            resulting_path = os.path.join(resulting_path, '..')
    else:
        resulting_path = '.'

    for element in tail_parts:
        resulting_path = os.path.join(resulting_path, element)

    return resulting_path
