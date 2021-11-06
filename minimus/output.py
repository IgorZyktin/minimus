# -*- coding: utf-8 -*-

"""Модуль для вывода сообщений на экран.
"""

from colorama import Fore

from minimus import constants


def greeting_message() -> None:
    """Распечатать приветствие."""
    separation_line()
    print(Fore.LIGHTRED_EX + constants.LOGO)
    print(Fore.LIGHTRED_EX + f'Version: {constants.__version__}')
    separation_line()


def setup(source: str, target: str,
          force_notes: bool, force_media: bool) -> None:
    """Вывести на экран стартовые настройки скрипта."""
    print(f' Исходники: {source}')
    print(f'Результаты: {target}')

    if force_notes:
        print(f'Включена принудительная перезапись файлов с заметками')

    if force_media:
        print(f'Включена принудительная перезапись вспомогательных файлов')


def separation_line() -> None:
    """Вывести на экран горизонтальную линию."""
    print(Fore.LIGHTRED_EX + constants.LINE)


def header(text: str) -> None:
    """Вывести новый блок текста."""
    print()
    print(Fore.CYAN + text)


def final_message(seconds: float) -> None:
    """Вывести на экран сообщение об окончании работы программы."""
    separation_line()
    print(Fore.LIGHTRED_EX + f'Обработка заняла {seconds:0.2f} сек.')
    separation_line()


def warnings(lines: list[str]) -> None:
    """Вывести на экран предупреждения."""
    for line in lines:
        print(f'\t{line}')
    print()
