"""Модуль по работе с файловой системой.
"""
import os
import sys
from pathlib import Path

from minimus.src import constants
from minimus.src import objects


def get_path() -> Path:
    """Верни корневой каталог, в котором хранятся заметки."""
    match sys.argv:
        case [_]:
            raw_path = '..'
        case [_, raw_path]:
            pass
        case _:
            msg = 'Для запуска Minimus требуется указать корневой каталог'
            raise ValueError(msg)

    match raw_path:
        case '.':
            path = Path(os.getcwd())
        case _:
            path = Path(raw_path)

    if not path.exists():
        msg = f'Указанный путь не существует: {path.absolute()!r}'
        raise FileNotFoundError(msg)

    if not path.is_dir():
        msg = f'Указанный путь это файл, а не каталог: {path.absolute()!r}'
        raise FileNotFoundError(msg)

    return path


def get_files(path: Path) -> list[objects.File]:
    """Собрать файлы."""
    files = []
    _recursively_dig(path, path, files)
    return files


def _recursively_dig(
        root: Path,
        path: Path,
        files: list[objects.File],
) -> None:
    """Рекурсивно собрать данные по всем файлам в каталоге."""
    entries: list[str] = os.listdir(path)

    for name in entries:
        sub_path = path / name

        if sub_path.is_file():
            if can_handle_this(name):
                new_file = objects.File(
                    path=sub_path,
                    root=root,
                )
                files.append(new_file)
        else:
            if name != constants.TAGS_FOLDER:
                _recursively_dig(root, sub_path, files)


def can_handle_this(name: str) -> bool:
    """Вернуть True если мы умеем обрабатывать такие файлы."""
    if name.lower().startswith(constants.IGNORED_PREFIXES):
        return False

    if not name.lower().endswith(constants.SUPPORTED_EXTENSIONS):
        return False

    if name == constants.README_FILENAME:
        return False

    return True


def ensure_folder_for_tags(path: Path) -> None:
    """Создать каталог для тегов, если такового нет."""
    (path / constants.TAGS_FOLDER).mkdir(exist_ok=True)
