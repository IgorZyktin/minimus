# -*- coding: utf-8 -*-

"""Инструменты работы с файловой системой.
"""
import os
from pathlib import Path
from typing import Optional

from colorama import Fore

from minimus.utils.output_processing import stdout


def get_ext(filename: str) -> str:
    """Вернуть расширение файла.

    >>> get_ext('something.txt')
    'txt'
    """
    _, ext = os.path.splitext(filename.lower())
    return ext.lstrip('.')


def join(path: str, filename: str) -> str:
    """Сшить путь с именем файла.

    Просто укороченная форма записи стандартной инструкции.
    """
    return os.path.join(path, filename)


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
            current_path = join(current_path, part)

        if not os.path.exists(current_path):
            os.mkdir(current_path)
            stdout('New folder created: {folder}',
                   folder=current_path, color=Fore.MAGENTA)

    return current_path


def find_shortest_common_path(current_directory: str,
                              target_directory: str) -> str:
    """Собрать минимально возможный по длине относительный путь из двух путей.

    >>> current = r"C:\\usr\\va"
    >>> target = r"C:\\usr\\va\\bg\\doc\\pictures\\ew"
    >>> find_shortest_common_path(current, target)
    '.\\bg\\doc\\pictures\\ew'
    """
    if current_directory == target_directory:
        return '.'

    head_parts = list(Path(current_directory).parts)
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
