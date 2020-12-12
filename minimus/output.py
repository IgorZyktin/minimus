# -*- coding: utf-8 -*-

"""Блоки вывода описаний на экран.
"""
from functools import partial

from colorama import Fore

from minimus import settings
from minimus.utils.output_processing import stdout


def start() -> None:
    """Вывести на экран сообщение о старте программы.
    """
    _stdout = partial(stdout, color=Fore.LIGHTRED_EX)
    _stdout(settings.LINE)
    _stdout(settings.LOGO)
    _stdout('Version: ' + settings.__version__)
    _stdout(settings.LINE)


def resulting_settings() -> None:
    """Вывести на экран получившиеся в итоге настройки программы.
    """
    _stdout = partial(stdout, color=Fore.CYAN)
    _stdout('Script started at: {folder}', folder=settings.LAUNCH_DIRECTORY)
    _stdout('Source directory: {folder}', folder=settings.SOURCE_DIRECTORY)
    _stdout('Output directory: {folder}', folder=settings.TARGET_DIRECTORY)
    _stdout('README.md directory: {folder}', folder=settings.README_DIRECTORY)


def line() -> None:
    """Вывести на экран разделительную линию.
    """
    stdout(settings.LINE, color=Fore.LIGHTRED_EX)


def newline() -> None:
    """Сделать перенос строки.
    """
    stdout('')


def complete() -> None:
    """Вывести на экран сообщение об окончании работы программы.
    """
    _stdout = partial(stdout, color=Fore.LIGHTRED_EX)
    _stdout('Processing complete')
    _stdout(settings.LINE)
