# -*- coding: utf-8 -*-

"""Tools created to show something on screen.
"""
from functools import partial

from colorama import Fore

from minimus import settings
from minimus.utils.output_processing import stdout


def show_greeting_message() -> None:
    """Output greeting message on screen."""
    _stdout = partial(stdout, color=Fore.LIGHTRED_EX)
    _stdout(settings.LINE)
    _stdout(settings.LOGO)
    _stdout('Version: {version}', version=settings.__version__)
    _stdout(settings.LINE)


def show_resulting_settings() -> None:
    """Output resulting settings on screen."""
    _stdout = partial(stdout, color=Fore.CYAN)
    _stdout('  Script started at: {folder}', folder=settings.LAUNCH_DIRECTORY)
    _stdout('   Source directory: {folder}', folder=settings.SOURCE_DIRECTORY)
    _stdout('   Output directory: {folder}', folder=settings.TARGET_DIRECTORY)
    _stdout('README.md directory: {folder}', folder=settings.README_DIRECTORY)


def show_separation_line() -> None:
    """Output horizontal line on screen.
    """
    stdout(settings.LINE, color=Fore.LIGHTRED_EX)


def show_user_files_rendering() -> None:
    """Output message about the fact that we render user files.
    """
    stdout('Saving original files:', color=Fore.BLUE)


def show_auto_files_rendering() -> None:
    """Output message about the fact that we render auto created files.
    """
    stdout('')
    stdout('Saving generated files:', color=Fore.BLUE)


def show_index_files_rendering() -> None:
    """Output message about the fact that we render index files.
    """
    stdout('')
    stdout('Saving indexes:', color=Fore.BLUE)


def show_final_message(seconds: float) -> None:
    """Вывести на экран сообщение об окончании работы программы.
    """
    _stdout = partial(stdout, color=Fore.LIGHTRED_EX)
    _stdout(settings.LINE)
    _stdout('Processing complete in {seconds} sec.', seconds=f'{seconds:0.2f}')
    _stdout(settings.LINE)
