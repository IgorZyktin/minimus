# -*- coding: utf-8 -*-

"""Блоки вывода описаний на экран.
"""
from typing import Callable

from minimus.config import Config


def describe_resulting_config(config: Config, stdout: Callable) -> None:
    """Вывести на экран получившиеся в итоге настройки программы.
    """
    stdout('Script started at: {folder}', folder=config.LAUNCH_DIRECTORY)
    stdout('Source directory: {folder}', folder=config.SOURCE_DIRECTORY)
    stdout('Output directory: {folder}', folder=config.TARGET_DIRECTORY)
    stdout('README.md directory: {folder}', folder=config.README_DIRECTORY)
