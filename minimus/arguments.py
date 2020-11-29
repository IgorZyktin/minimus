# -*- coding: utf-8 -*-

"""Инструменты разбора аргументов командной строки.

Приходится использовать argparse из-за желания иметь ноль
зависимостей для проекта. В норме я бы сделал сторонними средствами,
например через click.
"""
import argparse
from typing import List, Any, Dict

from minimus import settings
from minimus.utils.output_processing import stdout


def parse_command_line_arguments(raw_arguments: List[str]) -> Dict[str, Any]:
    """Вернуть словарь с аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description='Minumus launch arguments')

    parser.add_argument(
        '--lang',
        action='store',
        default='RU',
        choices=['EN', 'RU'],
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
        help='Where to save resulting files',
    )

    parser.add_argument(
        '--readme_directory',
        action='store',
        help='Where to save resulting README.md file',
    )

    args = parser.parse_args(raw_arguments[1:])

    return vars(args)


def apply_to_settings(arguments: Dict[str, Any]) -> None:
    """Применить полученные аргументы к настройкам.

    После этой операции настройки уже никогда больше не меняются.
    """
    settings.LANGUAGE = arguments.get('lang') or settings.LANGUAGE

    settings.SOURCE_DIRECTORY = (
            arguments.get('source_directory') or settings.SOURCE_DIRECTORY
    )

    settings.TARGET_DIRECTORY = (
            arguments.get('target_directory') or settings.TARGET_DIRECTORY
    )

    settings.README_DIRECTORY = (
            arguments.get('readme_directory') or settings.README_DIRECTORY
    )


def describe_resulting_settings() -> None:
    """Вывести на экран получившиеся в итоге настройки программы.
    """
    stdout('Script has been started at folder: {folder}',
           folder=settings.LAUNCH_DIRECTORY)
    stdout('Source directory: {folder}', folder=settings.SOURCE_DIRECTORY)
    stdout('Output directory: {folder}', folder=settings.TARGET_DIRECTORY)
    stdout('README.md directory: {folder}', folder=settings.README_DIRECTORY)
