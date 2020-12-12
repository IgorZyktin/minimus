# -*- coding: utf-8 -*-

"""Инструменты разбора аргументов командной строки.
"""
import argparse
from typing import List, Any, Dict

from minimus import settings


def parse_command_line_arguments(raw_arguments: List[str]) -> Dict[str, Any]:
    """Вернуть словарь с аргументами командной строки.
    """
    parser = argparse.ArgumentParser(
        description='Minimus: zettelkasten catalogue on markdown files',
    )

    parser.add_argument(
        '--language',
        action='store',
        default='RU',
        choices=['RU', 'EN'],
        help='Which language to use',
    )

    parser.add_argument(
        '--source_directory',
        action='store',
        help='Where to get source files from',
    )

    parser.add_argument(
        '--target_directory',
        action='store',
        help='Where to save resulting files to',
    )

    parser.add_argument(
        '--readme_directory',
        action='store',
        help='Where to save resulting README.md file to',
    )

    args = parser.parse_args(raw_arguments[1:])

    return vars(args)


def apply_cli_args_to_settings(arguments: Dict[str, Any]) -> None:
    """Применить полученные аргументы к настройкам.

    После этой операции настройки уже никогда больше не меняются.
    """

    def set_or_ignore(name: str):
        """Укороченная форма записи изменения параметра.
        """
        new_value = arguments.get(name)

        if new_value is not None:
            setattr(settings, name.upper(), new_value)

    set_or_ignore('language')
    set_or_ignore('source_directory')
    set_or_ignore('target_directory')
    set_or_ignore('readme_directory')
