"""Модуль для вывода сообщений на экран.
"""
from pathlib import Path

from minimus import constants


def greet() -> None:
    """Распечатать приветствие."""
    print_line()
    print(constants.LOGO)
    print_line()


def print_line() -> None:
    """Вывести на экран горизонтальную линию."""
    print(constants.LINE)


def print_path(path: Path) -> None:
    """Вывести на экран стартовые настройки скрипта."""
    print(f'Исходный каталог: {path.absolute()}')


def header(text: str) -> None:
    """Вывести новый блок текста."""
    print()
    print(text)


def complete(seconds: float) -> None:
    """Вывести на экран сообщение об окончании работы программы."""
    print_line()
    print(f'Обработка заняла {seconds:0.2f} сек.')
