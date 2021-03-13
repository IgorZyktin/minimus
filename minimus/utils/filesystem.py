# -*- coding: utf-8 -*-

"""Инструменты работы с файловой системой.
"""
import os
from pathlib import Path
from typing import Optional

from colorama import Fore

from minimus.utils.output_processing import stdout

__all__ = [
    'get_ext',
    'join',
    'ensure_folder_exists',
    'find_shortest_common_path',
]


def get_ext(filename: str) -> str:
    """Вернуть расширение файла.

    >>> get_ext('something.txt')
    'txt'
    """
    _, ext = os.path.splitext(filename.lower())
    return ext.lstrip('.')


def join(*args) -> str:
    """Сшить путь с именем файла.

    Просто укороченная форма записи стандартной инструкции.
    """
    return os.path.join(*args)






